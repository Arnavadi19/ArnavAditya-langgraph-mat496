# Code for the tutorials of 'Foundation: Introduction to LangGraph' course for MAT496 Monsoon 2025

## Module 1 Lesson 1: Motivation
Since there is no code for this lesson, I have not attached any links here.

An LLM is limited. It doesn't have access to tools, mutli step workflows, external context etc. We want LLMs to choose and pick their own control flows (or chains) depending on the problem that they face. An agent is a control flow defined by an LLM.

Langgraphs job is to give more control to the agent, while maintaining reilability. Langraph features: Persistence, Streaming, Human in the loop, Controllability.

## Module 1, Lesson 2: Simple Graph.
Link: [simple-graph.ipynb](./simple-graph.ipynb)
This notebook demonstrates building a simple LangGraph with 3 nodes using TypedDict state schema, conditional edges for routing, and the StateGraph class for compilation. Key concepts include nodes as Python functions that transform state, conditional edges that dynamically route between nodes based on logic, and the runnable protocol for graph execution.

## Module 1, Lesson 3: Langsmith studio
Link: [simple-graph.ipynb](./simple-graph.ipynb)
Installed Studio, learnt to navigate the UI and tweaked the graph a little bit then tried a couple of prompts to see how it works. 

## Module 1, Lesson 4: Chain
Learnt how to build a chain in lagngraph using chat messages as a state. Used add_messages for appending messages. 
For binding tools to the LLM, i used bind_tools() which lets the LLM choose to call a function for computation purposes based on the the users input.
created a complete tool execution cycle with conditional edges where the LLM makes tool calls, a separate node executes those tools and returns results, then the LLM provides a final response. Examples include building a math assistant that can perform addition and subtraction operations, demonstrating the four core concepts: chat messages as state, chat models in nodes, tool binding, and tool execution.