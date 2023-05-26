import typing
import abc


ResultType = typing.TypeVar('ResultType')


class ICommand(
		abc.ABC,
		typing.Generic[ResultType],
	):


	@abc.abstractmethod
	async def execute(self) -> ResultType:
		raise NotImplementedError()
