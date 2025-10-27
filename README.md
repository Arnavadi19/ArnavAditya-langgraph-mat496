# Code for the tutorials of 'Foundation: Introduction to LangGraph' course for MAT496 Monsoon 2025

# Module 1

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
Link: [chain.ipynb](./chain.ipynb)
Learnt how to build a chain in lagngraph using chat messages as a state. Used add_messages for appending messages. 
For binding tools to the LLM, i used bind_tools() which lets the LLM choose to call a function for computation purposes based on the the users input.
created a complete tool execution cycle with conditional edges where the LLM makes tool calls, a separate node executes those tools and returns results, then the LLM provides a final response. Examples include building a math assistant that can perform addition and subtraction operations, demonstrating the four core concepts: chat messages as state, chat models in nodes, tool binding, and tool execution.

## Module 1, Lesson 5: Router
Link: [router.ipynb](./router.ipynb)
Learned to extedn graphs by using tool-calling nodes and conditional edges that route to these tool-calling nodes.

This notebook demonstrates building a router-based agent that uses conditional routing to decide between direct responses or tool calls. Key learnings include using ToolNode and tools_condition from langgraph.prebuilt to simplify tool execution and routing logic. The graph routes to a tools node when the LLM makes tool calls, or directly to END for natural language responses, showing how LLMs can control program flow. The notebook introduces the concept of agents where the LLM acts as a router, directing execution based on user input requirements.

## Module 1, Lesson 6: Agent
Link: [agent.ipynb](./agent.ipynb)
ReAct: let the model observe the output from a tool call and then make decisions on what to do next.
The key difference from the router is adding an edge from tools back to assistant, creating a cycle that allows the agent to call multiple tools sequentially and reason about their outputs. This implements the act → observe → reason pattern, enabling complex multi-step problem solving like sequential arithmetic operations.

The text analysis cell creates a ReAct agent with three text processing tools (word count, character count, keyword extraction) that can analyze text comprehensively. It demonstrates how the agent can use multiple tools in sequence and combine their outputs to provide a complete text analysis report.

## Module 1, Lesson 7: agent with memory
Link: [agent-memory.ipynb](./agent-memory.ipynb)

This notebook introduces persistence and memory to LangGraph agents using checkpointers to save graph state after each step. The key concept is that without memory, each graph execution is independent and transient, preventing multi-turn conversations. By compiling the graph with a MemorySaver checkpointer and using thread_id configuration, the agent can maintain conversation history across multiple invocations. This enables contextual follow-up queries like "Multiply that by 2" where the agent remembers previous results (like "that" referring to the sum of 3 and 4 being 7). The checkpointer writes state at every graph step, allowing the agent to pick up from the last checkpoint when continuing a conversation thread.

# Module 2: State and Memory

## Module 2, Lesson 1: State Schema
Link: [state-schema](./state-schema.ipynb)

This notebook introduces State Schema, which represents the structure and the types of data that will be used in a graph.
TypedDicts provide a way to  define dictionaries with a fixed set of keys and specific value types for each key. Dataclasses are another way of defining the type of data in a graph. The problem with these 2 is that they dont enforce type checking at runtime.

So, we use pydantic for defining state schemas to fix this problem.

## Module 2, Lesson 2: State Reducers

Link: [state-reducers](./state-reducers.ipynb)

In this lesson we faced a problem while trying to overwrite the graph state on 2 different nodes, since there is no preferred way to perform these updates.Reducers solve this by specifyng a way to perform updates. Custom reducers further help in combining lists where the input may be None type.

Next, We also cover the built-in add_messages reducer for message handling, which supports appending, re-writing messages by ID, and removal using RemoveMessage.

## Module 2, Lesson 3: Multiple Schemas

Link: [multiple-schemas](./multiple-schemas.ipynb)

Dy default, all graph nodes use a single schema. We use multiple schemas like PrivateState for passing intermediate data b/w nodes that isnt needed in graph input/output. Next, we saw an example where there were different input and output schema. This exposes the graph API to specific fields whereas the internal nodes can work with a full Overall State.

Added an example cell for displaying my learning from this video which achieves the above mentioned.

## Module 2, Lesson 4: Trim and filter messages

Link: [trim-filter-messages](./trim-filter-messages.ipynb)

This notebook addresses managing long-running conversations to avoid high token usage and latency. 
Three approaches are demonstrated: RemoveMessage with add_messages reducer to delete old messages from state, message filtering to pass only specific messages (e.g., messages[-1:]) to the model without modifying state, and trim_messages to restrict conversation history to a specified token count. 
The key difference is filtering/trimming happens at model invocation while RemoveMessage modifies the graph state itself.

## Module 2, Lesson 5: Chatbot w/ summarizing messages and memory

Link: [chatbot-summarization](./chatbot-summarization.ipynb)

In this notebook, we built a chatbot with conversation summarization and memory for handling long running convos.
This chatbot uses a custom state schema with summary key which gets updated when conversation exceeds 6 messages. 
The graph uses MemorySaver checkpointer with Thread IDs to maintain conversation states across multiple invocations/. This helps to compress conversation history hence reducing token usage while preserving context.

## Module 2, Lesson 6: Chatbot with summarizing messages and external memory

Link: [chatbot-external-memory](./chatbot-external-memory.ipynb)

The core idea here is linking a DB such as sqlite to have a persistent memory for a chatbot. We connected to the database, then created a checkpointer.
By using a persistent SQLite database (either in-memory with ":memory:" or on-disk with a file path), the conversation state survives beyond the program lifecycle and can be reloaded even after restarting the notebook kernel. 
This enables indefinite memory persistence where conversations can be resumed across sessions using the same thread_id, making it suitable for production chatbots that need long-term user memory.


# Module 3: UX and HITL

## Module 3, Lesson 1: Streaming

Link: [streaming-interruption](./module-3/streaming-interruption.ipynb)

Learnt what streaming is, with multiple modes like "values" which streams full state after each node, "updates" which streams only state changes. astream_events() enables token-level streaming. 
Also learnt the LangGraph API streaming using the SDK client, including "messages" stream mode. It simplifies  handling message events with complete and partial event types.

## Module 3, Lesson 2: Breakpoints

LInk: [breakpoints](./module-3/breakpoints.ipynb)

This video introduces breakpoints for human-in-the-loop approval by compiling graphs with interrupt_before=["node_name"] or interrupt_after, which pauses execution at specified nodes. When interrupted, you can inspect state using graph.get_state(thread), check state.next to see the next node, and resume execution by passing None as input to graph.stream(), which continues from the last checkpoint. This enables approval workflows where users can review agent actions (like tool calls) before allowing them to proceed, supporting use cases for debugging, approval, and state editing.

## Module 3, Lesson 3: Editing State and Human Feedbacks

LInk: [edit-state-human-feedback.ipynb](./module-3/edit-state-human-feedback.ipynb)


This notebook demonstrates editing graph state after breakpoints using graph.update_state() to modify state (like adding/overwriting messages) before resuming execution. 
It introduces a human feedback pattern where a no-op human_feedback node with interrupt_before serves as a placeholder for collecting user input, and update_state(..., as_node="human_feedback") applies the feedback as if that node executed it. 
This enables workflows where humans can correct agent decisions, provide additional context, or change instructions mid-execution, with the agent seamlessly incorporating the feedback and continuing from where it left off.
On the final breakpoint cell, gave a message to divide instead of multiplying 2 numbers.



## Module 3, Lesson 4: Dynamic Breakpoints

Link: [dynamic-breakpoints](./module-3/dynamic-breakpoints.ipynb)

We use dynamic breakpoints using NodeInterrupt, which allows nodes to conditionally interrupt themselves based on runtime logic like checking input length). Unlike static breakpoints set during compilation with interrupt_before/after, NodeInterrupt is raised from within a node and can pass custom messages explaining why the interruption occurred. To resume after a NodeInterrupt, you must update the state using graph.update_state() to change the condition that caused the interruption, otherwise the node will keep re-running and hitting the same interrupt.

