import typing
import asyncio


ResultType = typing.TypeVar('ResultType')


def _copy_future(future: asyncio.Future[ResultType]) -> asyncio.Future[ResultType]:

	if not future.done():

		async def __copy_future() -> ResultType:
			return await future

		return asyncio.ensure_future(__copy_future())

	future = future.get_loop().create_future()

	if future.cancelled():
		future.cancel()
		return future

	if future.exception() is not None:
		future.set_exception(typing.cast(Exception, future.exception()))
		return future

	future.set_result(future.result())
	return future
