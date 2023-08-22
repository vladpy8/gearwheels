import typing
import asyncio
from collections import deque

from gearwheels.machine._conceal_future_return import conceal_future_return


class FutureSet:


	def __init__(self):

		self.__future_set: deque[asyncio.Future[None]] = deque()


	def empty(self) -> bool:
		return len(self.__future_set) == 0


	def add(
			self,
			future: asyncio.Future[typing.Any],
		) -> None:

		self.__future_set.append(conceal_future_return(future))


	def clear(
			self,
			complete_f: bool = False,
		) -> asyncio.Future[None]:

		#TODO simplify

		future_queue = deque((future for future in self.__future_set if future.done() or complete_f))
		self.__future_set = deque((future for future in self.__future_set if not (future.done() or complete_f)))

		async def __dispose_async() -> None:

			try:

				while len(future_queue) > 0:
					future = future_queue.popleft()
					await future

			except:

				for future in future_queue:
					self.add(future)

				raise

		disposal_future = asyncio.create_task(__dispose_async())
		return disposal_future
