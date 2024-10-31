from src.agent.models import Agent


def get_task_prompt() -> str:
    prompt = """Process this task: {description}. Output should be only depend on the task. Try to not include descriptions."""

    return prompt.strip()


def get_comment_task_prompt() -> str:
    prompt = """Provide exactly one short sentence starting with "Task is successfully completed, and..." that only confirms task completion and information relevance. Do not include details, summaries, or recommendations. Example: "Task is successfully completed, and the gathered data matches the required criteria."
    """
    return prompt.strip()


def get_desc_prompt(
    agent: Agent, agent_instruction, previous_output, doc_context, webhook_urls
) -> str:
    prompt = f"""Process this task: {agent_instruction}. \n\nBegin by thoroughly reading and analyzing the provided instructions and task. Your approach should prioritize clarity, precision, and accuracy in gathering and presenting information. Focus exclusively on delivering concise, relevant insights that directly address the task requirements.\n\n"""

    if webhook_urls:
        prompt += f"### List of Webhook URL's for specific Tools ### \n{webhook_urls}. Take payload from the tasks. Do not change the payload."

    if doc_context:
        prompt += f"""### Context of Document Provided By User\nDocument: {doc_context}. \n\n"""

    prompt += f"""
    Below information is about the group information such as focus group survey, top ideas, api data and survey. Analyze the deatils provided and improve the overall output.\n ## Focus group survey: {agent.focus_group_survey}\n ## Top Ideas: {agent.top_idea}\n ## API Data: {agent.api_data}\n ## Survey: {agent.survey}\n."""

    if previous_output:
        prompt += f"""To provide additional context, consider the following previous output: {str(previous_output)}. Use this historical context to inform your analysis, ensuring continuity and building upon existing insights while avoiding redundancy. Your response should acknowledge and integrate relevant aspects of this previous work while maintaining focus on the current objectives."""

    return prompt.strip()


async def get_chat_bot_prompt(
    question, previous_queries, previous_responses, relevant_document
) -> str:
    prompt = f"""
            Assist the user with their question in a friendly and helpful manner: "{question}". 
            Use context from previous interactions to provide a more accurate response. Only mention previous interactions if it is necessary for understanding or clarification.

            ### Previous Chat History ###
            - Previous Questions: {previous_queries}
            - Previous Answers: {previous_responses}

            Please refer to this chat history to improve your response. For example, if the user mentions "he" or "she," and a person was mentioned earlier, assume they are referring to that person unless otherwise stated.

            """

    if relevant_document:
        prompt += f"""
                    ### Relevant Document Context ###
                    In addition to the chat history, use the following document context if it is related to the user's question for much better accuracy & precision:
                    {relevant_document}
                    """

    return prompt
