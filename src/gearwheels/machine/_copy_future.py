import typing
import asyncio


ResultType = typing.TypeVar('ResultType')


def _copy_future(future: asyncio.Future[ResultType]) -> asyncio.Future[ResultType]:

	if not future.done():

		async def __copy_future() -> ResultType:
			return await future

		return asyncio.ensure_future(__copy_future())

	future_copy = future.get_loop().create_future()

	if future.cancelled():
		future_copy.cancel()
		return future_copy

	if future.exception() is not None:
		future_copy.set_exception(typing.cast(Exception, future.exception()))
		return future_copy

	future_copy.set_result(future.result())
	return future_copy
