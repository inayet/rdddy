import asyncio
from rdddy.actor import Actor
from rdddy.actor_system import ActorSystem
from rdddy.messages import Message, ExceptionMessage, TerminationMessage


class WorkerActor(Actor):
    async def start_working(self):
        try:
            # Simulate some work
            await asyncio.sleep(1)
            # Simulate an error
            raise RuntimeError("Worker encountered an error.")
        except Exception as e:
            await self.publish(ExceptionMessage(content=str(e)))
            await self.publish(
                TerminationMessage(content=str(e), actor_id=self.actor_id)
            )


class SupervisorActor(Actor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)
        self.worker_actor = None
        self.restart_count = 0

    async def handle_message(self, message: ExceptionMessage):
        # If an error message is received, restart the worker
        if "error" in message.content:
            self.restart_count += 1
            self.worker_actor = await self.actor_system.actor_of(WorkerActor)

    async def start_worker(self):
        self.worker_actor = await self.actor_system.actor_of(WorkerActor)
        await self.worker_actor.start_working()


class RootSupervisorActor(Actor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)
        self.supervisor_actor = None
        self.restart_count = 0

    async def handle_message(self, message: ExceptionMessage):
        if "error" in message.content:
            self.restart_count += 1

    async def handle_termination(self, message: TerminationMessage):
        # Handle termination logic
        await self.actor_system.remove_actor(message.actor_id)

    async def start_supervisor(self):
        self.supervisor_actor = await self.actor_system.actor_of(SupervisorActor)
        await self.supervisor_actor.start_worker()


import pytest
from rdddy.actor_system import ActorSystem


@pytest.fixture
def actor_system(event_loop):
    return ActorSystem(event_loop)


@pytest.mark.asyncio
async def test_worker_restart(actor_system):
    root_supervisor = await actor_system.actor_of(RootSupervisorActor)
    await root_supervisor.start_supervisor()

    await asyncio.sleep(1)  # Give enough time for the hierarchy to react

    # Check if the supervisor has restarted the worker
    assert root_supervisor.restart_count > 0

    await asyncio.sleep(5)

    await asyncio.sleep(1)
    # Check if the root supervisor has restarted the supervisor
