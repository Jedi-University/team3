import asyncio
import random
import time

from orch.orch import Orch

class AsyncOrch(Orch):

    def run(self, worker, tasks: list) -> list:

        async def async_worker(worker, queue_in, queue_out, name):
            while True:
                task = await queue_in.get()
                print(f'{name} task {task}')
                await asyncio.sleep(0)
                r = worker(task)
                queue_out.put_nowait(r)
                queue_in.task_done()

        async def async_run(worker, tasks):

            queue_in = asyncio.Queue()
            queue_out = asyncio.Queue()

            for task in tasks:
                queue_in.put_nowait(task)

            async_tasks = []
            for i in range(self.max_workers):
                task = asyncio.create_task(async_worker(
                    worker, queue_in, queue_out, f'name{i}'))
                async_tasks.append(task)

            await queue_in.join()

            # Cancel our worker tasks.
            for task in async_tasks:
                task.cancel()
            # Wait until all worker tasks are cancelled.
            a = await asyncio.gather(*async_tasks, return_exceptions=True)

            result = []
            while queue_out.qsize():
                r = await queue_out.get()
                result.append(r)
                queue_out.task_done()

            await queue_out.join()
            return result

        result = asyncio.run(async_run(worker, tasks))
        return result
