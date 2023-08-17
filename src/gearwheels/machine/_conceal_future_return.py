import typing
import asyncio


def _conceal_future_return(future: asyncio.Future[typing.Any]) -> asyncio.Future[None]:

	async def __conceal_future_return_async() -> None:
		try:
			await future
		except:
			pass

	return asyncio.create_task(__conceal_future_return_async())
