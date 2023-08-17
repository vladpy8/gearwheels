import typing
import asyncio


ResultType = typing.TypeVar('ResultType')


def _conceal_future(future: asyncio.Future[ResultType]) -> asyncio.Future[ResultType]:

	async def __conceal_future_async() -> ResultType:
		return await future

	return (
		asyncio.shield(
			asyncio.create_task(
				__conceal_future_async()
			)
		)
	)
