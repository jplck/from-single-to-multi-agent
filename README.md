# From Single to Multi-Agent AI Systems

This repository contains a comprehensive collection of labs and resources for learning about AI agent development, from single-agent implementations to complex multi-agent systems. It explores various frameworks including Semantic Kernel, AutoGen, and more, demonstrating practical implementations of modern AI agent architectures.

## Overview

The repository is structured to provide a progressive learning journey through the world of AI agents:

- **Foundation concepts**: Learn about basic agent patterns like ReAct
- **Advanced frameworks**: Explore Semantic Kernel, process frameworks, and AutoGen
- **Multi-agent orchestration**: Discover techniques for coordinating multiple specialized agents

## Lab Structure

The labs are organized in increasing complexity, starting from basic concepts and advancing to sophisticated multi-agent systems:

| Lab | Description | Link |
|-----|-------------|------|
| Azure OpenAI Basics | Introduction to working with Azure OpenAI | [01-basics/01_azureopenai.ipynb](labs/01-basics/01_azureopenai.ipynb) |
| Semantic Kernel - Orchestration | Learn to orchestrate AI capabilities with Semantic Kernel | [02-semantic-kernel/01_orchestrator.ipynb](labs/02-semantic-kernel/01_orchestrator.ipynb) |
| Semantic Kernel - Functions | Working with functions in Semantic Kernel | [02-semantic-kernel/02_functions.ipynb](labs/02-semantic-kernel/02_functions.ipynb) |
| Semantic Kernel - Multi-modal | Handling multi-modal content with Semantic Kernel | [02-semantic-kernel/03_multi-modal.ipynb](labs/02-semantic-kernel/03_multi-modal.ipynb) |
| Planner | Implementing AI planning capabilities | [03-planner/01_planner.ipynb](labs/03-planner/01_planner.ipynb) |
| Agent Framework - Basic Agents | Building individual agents with Semantic Kernel | [04-agent-framework/01_agents.ipynb](labs/04-agent-framework/01_agents.ipynb) |
| Agent Framework - Group Chat | Implementing collaborative agent conversations | [04-agent-framework/02_agents-group-chat.ipynb](labs/04-agent-framework/02_agents-group-chat.ipynb) |
| Process Framework - Basics | Understanding the Semantic Kernel Process Framework | [05-process-framework/01_process.ipynb](labs/05-process-framework/01_process.ipynb) |
| Process Framework - Advanced | Building complex workflows with the Process Framework | [05-process-framework/02_process.ipynb](labs/05-process-framework/02_process.ipynb) |
| AutoGen - Simple Group | Creating basic agent groups with AutoGen | [06-autogen/01_autogen-simple-group.ipynb](labs/06-autogen/01_autogen-simple-group.ipynb) |
| AutoGen - Group Chat | Building multi-agent conversations with AutoGen | [06-autogen/02_autogen-group-chat.ipynb](labs/06-autogen/02_autogen-group-chat.ipynb) |
| AutoGen - Reasoning | Implementing advanced reasoning with AutoGen | [06-autogen/03_autogen-reasoning.ipynb](labs/06-autogen/03_autogen-reasoning.ipynb) |
| Single React Agent | Implementation of a basic ReAct pattern agent | [Single React Agent](labs/single_react_agent) |

## Key Concepts Covered

### Single-Agent Example

- **ReAct (Reasoning + Acting)** - Combining reasoning with tool use for more effective agents
- Function/tool calling capabilities
- State management within agents

### Semantic Kernel Framework

- Creating kernel functions and tools
- Building specialized agents with specific roles
- Orchestrating multi-agent interactions
- Process framework for structured AI workflows

### Process Framework

- Event-driven design for AI workflows
- State management across process steps
- Conditional branching and error handling
- Complex workflow orchestration

### Multi-Agent Architectures

- Specialized agent roles and responsibilities
- Agent coordination and communication
- Multi-agent problem solving through collaboration
- Group chat implementations

### AutoGen Framework

- Building agent groups
- Implementing conversational agents
- Advanced reasoning capabilities

## Getting Started

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. (Optional) Configure your Azure OpenAI credentials in a `.env` file
4. Start exploring the labs sequentially, beginning with the single agent implementation

## Azure Integration (Optional)

This repository includes infrastructure templates for deploying solutions to Azure:
- Azure OpenAI services configuration
- Container Apps environments
- Storage and hosting services