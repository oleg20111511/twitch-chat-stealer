import settings
from twitchio.ext import commands
from sqlalchemy.orm import Session

from models import Message, engine


class Bot(commands.Bot):
	messages_to_save = []

	async def event_ready(self):
		print(f'Logged in as | {self.nick}')


	async def event_message(self, ctx):
		'''
		Save received messages in database
		'''

		# Filter out some messages
		failures = [
			ctx.content.startswith('!'),
			ctx.author.is_mod
		]
		if any(failures):
			return

		# Create message
		msg = Message(
			source=str(ctx.channel),
			sender=str(ctx.author.name),
			content=str(ctx.content)
		)
		print(f"Added message to list:\n{msg}")

		# Add message to queue
		self.messages_to_save.append(msg)

		# Flush queue when it gets big enough
		if len(self.messages_to_save) > settings.FLUSH_SIZE:
			print('--Flushing messages')
			with Session(engine) as session:
				session.bulk_save_objects(self.messages_to_save)
				session.commit()
			self.messages_to_save = []


if __name__ == "__main__":
	bot = Bot(
		token=settings.TOKEN,
		prefix=settings.PREFIX,
		initial_channels=settings.INITIAL_CHANNELS
	)
	bot.run()
