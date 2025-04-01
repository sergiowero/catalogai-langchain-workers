import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Type

from pydantic import BaseModel, ConfigDict
from typing_extensions import TypeAliasType

Id = TypeAliasType('Id', str)
Input = TypeAliasType('Input', dict[str, Any])


class TaskError(Exception):
    """Raised when a task fails to execute."""

    def __init__(self, task_id: str, error: Exception, result: Any = None):
        self.task_id = task_id
        self.error = error
        self.result = result
        super().__init__(f"Task '{task_id}' failed: {str(error)}")


class TaskRunnable(BaseModel):
    """Base class for task implementations."""

    async def run(self, input: Input) -> Any:
        """Execute the task with the given input."""
        raise NotImplementedError('Subclasses must implement run')

    async def on_complete(self, input: Input, result: Any) -> None:
        """Called when the task completes, regardless of success or failure."""
        pass

    async def on_success(self, input: Input, result: Any) -> None:
        """Called when the task succeeds."""
        pass

    async def on_fail(self, input: Input, error: Exception, result: Any) -> None:
        """Called when the task fails."""
        pass


class CallableTaskRunnable(TaskRunnable):
    """Convenience class for creating task implementations from callables."""

    func: Callable[[Input], Any]
    on_complete_func: Callable[[Input, Any], Any] | None
    on_success_func: Callable[[Input, Any], Any] | None
    on_fail_func: Callable[[Input, Exception, Any], Any] | None

    async def run(self, input: Input) -> Any:
        result = self.func(input)
        if asyncio.iscoroutine(result):
            return await result
        return result

    async def on_complete(self, input: Input, result: Any) -> None:
        if self.on_complete_func:
            result = self.on_complete_func(input, result)
            if asyncio.iscoroutine(result):
                return await result
            return result

    async def on_success(self, input: Input, result: Any) -> None:
        if self.on_success_func:
            result = self.on_success_func(input, result)
            if asyncio.iscoroutine(result):
                return await result
            return result

    async def on_fail(self, input: Input, error: Exception, result: Any) -> None:
        if self.on_fail_func:
            result = self.on_fail_func(input, error, result)
            if asyncio.iscoroutine(result):
                return await result
            return result


class Task(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Id
    implementation: TaskRunnable | List[TaskRunnable]
    output_name: str
    concurrency_limit: int | None
    fail_fast: bool = True

    def __hash__(self) -> int:
        return hash(self.id)

    async def run(self, input: Input) -> Any:
        """Execute the task with the given input."""
        impl = self.implementation

        # Handle single implementation
        if not isinstance(impl, list):
            return await self._run_single(input, impl)

        # Handle multiple implementations
        tasks = [self._run_single(input, item) for item in impl]

        # Run with concurrency limit
        if self.concurrency_limit is not None:
            return await self._run_with_concurrency_limit(tasks)
        else:
            return await asyncio.gather(*tasks)

    async def _run_single(self, input: Input, impl: Type[TaskRunnable]) -> Any:
        """Run a single implementation."""
        try:
            # Instantiate the implementation class
            obj = impl()
            result = await obj.run(input)

            # Call success hook
            await obj.on_success(input, result)

            return result

        except Exception as e:
            await impl().on_fail(input, e, None)
            raise TaskError(self.id, e)

        finally:
            # Always call on_complete
            await impl().on_complete(input, None)

    async def _run_with_concurrency_limit(self, tasks: List[Awaitable]) -> List[Any]:
        """Run tasks with concurrency limit."""
        results = []
        semaphore = asyncio.Semaphore(self.concurrency_limit)

        async def run_task(task: Awaitable) -> Any:
            async with semaphore:
                return await task

        for task in tasks:
            results.append(run_task(task))

        return await asyncio.gather(*results)


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Id
    tasks: List[Task]

    async def run(self, input_data: Input) -> Dict[str, Any]:
        """
        Execute the workflow with a single input.

        Args:
            input_data: Dictionary containing the input data for the workflow

        Returns:
            Dictionary mapping output names to their results

        Raises:
            TaskError: If any task fails to execute
        """
        results: Dict[str, Any] = {}

        # Initialize the context with input data
        context: Input = {**input_data}

        # Execute tasks in sequence
        for task in self.tasks:
            try:
                # Get input parameters for this task
                task_input = {**context}

                # Execute the task
                result = await task.run(task_input)

                # Store the result
                results[task.output_name] = result

                # Update context with the result
                context[task.output_name] = result

            except TaskError:
                if task.fail_fast:
                    raise
                results[task.output_name] = None

        return results
