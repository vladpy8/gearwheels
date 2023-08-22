import typing
import asyncio


def conceal_future_return(future: asyncio.Future[typing.Any]) -> asyncio.Future[None]:

	async def conceal_future_return_async() -> None:
		try:
			await future
		except BaseException:
			pass

	return asyncio.create_task(conceal_future_return_async())
