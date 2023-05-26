import asyncio
import typing


def _conceal_future_return(
		future: typing.Awaitable[typing.Any]
	) -> asyncio.Future[None]:

	async def _conceal_future_return_async() -> None:
		await future
		pass

	return asyncio.create_task(_conceal_future_return_async())
