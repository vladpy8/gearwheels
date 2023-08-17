import abc
import typing
import asyncio

from gearwheels.machine.error import MustStartError
from gearwheels.machine.future_set import FutureSet

from gearwheels.machine._conceal_future import _conceal_future


ResultType = typing.TypeVar('ResultType')


class ParallelMachine(
		abc.ABC,
		typing.Generic[ResultType],
	):


	def __init__(
			self,
		):

		super().__init__()

		self.__start_future: typing.Optional[asyncio.Future[None]] = None
		self.__stop_future: typing.Optional[asyncio.Future[None]] = None

		self.__future_set = FutureSet()


	@typing.final
	def start(self) -> asyncio.Future[None]:

		if self.__start_future is not None:
			return _conceal_future(self.__start_future)

		stop_future = None
		if self.__stop_future is not None:
			stop_future = self.__stop_future
			self.__stop_future = None

		async def __start_async() -> None:

			if stop_future is not None:
				await stop_future

			await self._start()

		self.__start_future = asyncio.create_task(__start_async())

		return _conceal_future(self.__start_future)


	@typing.final
	def stop(self) -> asyncio.Future[None]:

		if self.__stop_future is not None:
			return _conceal_future(self.__stop_future)

		if self.__start_future is None:
			return asyncio.ensure_future(asyncio.sleep(0, None))

		start_future = self.__start_future
		self.__start_future = None

		execute_complete_future = self.__future_set.clear(complete_f=True,)

		async def __stop_async() -> None:

			await start_future
			await execute_complete_future

			# TODO bug?
			# hacky
			if self.__stop_future is stop_future:
				self.__stop_future = None

			await self._stop()

		self.__stop_future = asyncio.ensure_future(__stop_async())
		stop_future = self.__stop_future

		return _conceal_future(self.__stop_future)


	@typing.final
	def execute(self) -> asyncio.Future[ResultType]:

		if self.__start_future is None:
			raise MustStartError()

		start_future = self.__start_future

		async def __execute_async() -> ResultType:

			await start_future

			return await self._execute()

		execute_future = asyncio.create_task(__execute_async())
		self.__future_set.add(execute_future)

		return _conceal_future(execute_future)


	async def _start(self) -> None:
		pass


	async def _stop(self) -> None:
		pass


	@abc.abstractmethod
	async def _execute(self) -> ResultType:
		pass
