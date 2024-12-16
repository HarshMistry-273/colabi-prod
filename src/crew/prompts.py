from src.agent.models import Agent


def get_task_prompt() -> str:
    prompt = """Process the following task: {description}. Provide an output strictly dependent on the task's context, without including explanations or descriptions beyond what the task requires."""

    return prompt.strip()


def get_comment_task_prompt() -> str:
    prompt = """Respond with exactly one concise sentence starting with 'Task is successfully completed, and...' to confirm only task completion and information relevance, without adding details, summaries, or suggestions."
    """
    return prompt.strip()


def get_desc_prompt(
    agent: Agent, agent_instruction, previous_output, doc_context, params
) -> str:
    prompt = f"""Process the following task: {agent_instruction}. Thoroughly analyze the provided instructions to ensure clarity, precision, and accuracy in your response. Deliver concise and relevant insights that directly fulfill the task requirements, adhering to the following strict guidelines: \n1. Do not hallucinate: Provide only factual and accurate responses based on the given input or instructions. If there is insufficient data or context to complete the task, explicitly state: Sorry, couldn't complete the task because of [specific reason]. \n2. Output Format:\n- Use Markdown formatting.\n- Start with a heading formatted as ### [Task Title or Output Summary].\n- Provide the main content as normal text, bullet points, or tables where appropriate.\n- Ensure your response remains focused, avoids unnecessary elaborations, and maintains alignment with the task's core requirements.\n- If the provided data appears to be incomplete, nonsensical, or dummy placeholders (e.g., "asd, adj, asd"), clearly inform the user about this issue and avoid generating a dummy or irrelevant response."""

    if doc_context:
        prompt += f"""Context: {doc_context}\n\nInstruction: Based on the provided context, respond or process the information strictly adhering to the details and scope of the document. Ensure the response aligns closely with the content and avoids adding unrelated explanations or assumptions."""

    prompt += f"""Analyze the provided group information, which includes data from a focus group survey, top ideas, API data, and a general survey. Synthesize the details to enhance the overall insights and recommendations. Use the following structured inputs:\n Focus Group Survey: {agent.focus_group_survey}\nTop Ideas: {agent.top_idea}\nAPI Data: {agent.api_data}\nSurvey: {agent.survey}\nProvide a comprehensive and actionable output based on the analysis."""

    if previous_output:
        prompt += f""""Using the provided historical context: {str(previous_output)}, build upon the existing insights to deliver a focused analysis. Ensure continuity by integrating relevant aspects of the previous work while avoiding redundancy. Your response should prioritize the current objectives and provide a seamless progression of ideas."""
    if params:
        prompt += params

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
