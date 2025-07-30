"""
Resolves threads.
"""

from bot.agents.agent_manager import AgentManager


async def resolve_thread(thread_id: int, agent_manager: AgentManager):
    """
    Resolve a thread and trigger the insight-learning process.

    Args:
        thread_id (int): The ID of the thread to resolve.
        agent_manager (AgentManager): The agent manager.

    """
    thread = await agent_manager.bot.fetch_thread(thread_id)
    if not thread:
        return

    # Get insights from the current thread
    insights = await agent_manager.support_agent.get_insights_from_thread(thread)

    # Update the insights channel
    await agent_manager.support_agent.update_insights_channel(insights)

    # Archive the thread
    await thread.edit(archived=True)
