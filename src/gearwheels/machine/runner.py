import typing
import asyncio

from gearwheels.machine.icommand import ICommand
from gearwheels.machine._conceal_future_return import _conceal_future_return


ResultType = typing.TypeVar('ResultType')


class Runner(typing.Generic[ResultType]):


	def __init__(
			self,
			run_command: ICommand[ResultType],
			block_count: typing.Optional[int] = None,
		):

		if (
				block_count is not None
				and block_count <= 0
			):
			raise ValueError('block count must be positive')

		self.run_command = run_command
		self.block_count = block_count

		self._count = 0
		self._run_future: typing.Optional[asyncio.Future] = None


	@property
	def count(self) -> int:
		return self._count


	def run(self) -> asyncio.Future[ResultType]:

		if (
				self.block_count is not None
				and self._count >= self.block_count
				and self._run_future is not None
			):

			self._count += 1
			return self._run_future

		self._count += 1

		prev_run_future = self._run_future
		self._run_future = None

		async def _execute_async():

			if prev_run_future is not None:
				await prev_run_future

			result = await self.run_command.execute()

			# hacky
			if (
					self.block_count is None
					and self._run_future is run_future
				):
				self._run_future = None

			return result

		run_future = asyncio.create_task(_execute_async())

		self._run_future = run_future

		if self.block_count is None:
			self._run_future = _conceal_future_return(self._run_future)

		return run_future
