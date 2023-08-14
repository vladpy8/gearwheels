import typing
import asyncio


def _conceal_future_return(future: asyncio.Future[typing.Any]) -> asyncio.Future[None]:

	async def __conceal_future_return_async() -> None:
		await future
		pass

	return asyncio.ensure_future(__conceal_future_return_async())
