"""Observability and monitoring for CrewAI agents."""
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


@dataclass
class AgentMetrics:
    """Metrics for a single agent."""
    agent_name: str
    task_count: int = 0
    tool_calls: int = 0
    total_time: float = 0.0
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    tools_used: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class TaskMetrics:
    """Metrics for a single task."""
    task_id: str
    task_description: str
    agent_name: str
    status: str = "pending"
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    duration: float = 0.0
    tool_calls: int = 0
    output_length: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class CrewObserver:
    """Observability tracker for CrewAI operations."""

    def __init__(self, enable_langsmith: bool = False):
        """Initialize the observer."""
        self.enable_langsmith = enable_langsmith
        self.start_time = time.time()
        self.end_time = None
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.task_metrics: List[TaskMetrics] = []
        self.events: List[Dict[str, Any]] = []

        # Token tracking (approximation)
        self.total_tokens_estimate = 0
        self.input_tokens_estimate = 0
        self.output_tokens_estimate = 0

    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Log an event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "time_elapsed": time.time() - self.start_time,
            "event_type": event_type,
            "data": data
        }
        self.events.append(event)

    def start_agent(self, agent_name: str):
        """Track when an agent starts."""
        if agent_name not in self.agent_metrics:
            self.agent_metrics[agent_name] = AgentMetrics(agent_name=agent_name)

        self.agent_metrics[agent_name].start_time = time.time()
        self.log_event("agent_start", {"agent": agent_name})

        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🤖 Agent Started: {agent_name}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    def end_agent(self, agent_name: str):
        """Track when an agent completes."""
        if agent_name in self.agent_metrics:
            metrics = self.agent_metrics[agent_name]
            metrics.end_time = time.time()
            if metrics.start_time:
                metrics.total_time = metrics.end_time - metrics.start_time

        self.log_event("agent_end", {"agent": agent_name})

    def start_task(self, task_id: str, task_description: str, agent_name: str):
        """Track when a task starts."""
        task = TaskMetrics(
            task_id=task_id,
            task_description=task_description[:100] + "..." if len(task_description) > 100 else task_description,
            agent_name=agent_name,
            status="running",
            start_time=time.time()
        )
        self.task_metrics.append(task)

        self.log_event("task_start", {
            "task_id": task_id,
            "agent": agent_name,
            "description": task_description[:100]
        })

        print(f"\n{Fore.YELLOW}📋 Task Started: {task.task_description}")
        print(f"{Fore.YELLOW}   Agent: {agent_name}{Style.RESET_ALL}")

    def end_task(self, task_id: str, status: str = "completed", output: str = ""):
        """Track when a task completes."""
        for task in self.task_metrics:
            if task.task_id == task_id:
                task.end_time = time.time()
                task.status = status
                task.output_length = len(output)
                if task.start_time:
                    task.duration = task.end_time - task.start_time

                # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
                output_tokens = len(output) // 4
                self.output_tokens_estimate += output_tokens
                self.total_tokens_estimate += output_tokens

                self.log_event("task_end", {
                    "task_id": task_id,
                    "status": status,
                    "duration": task.duration,
                    "output_length": len(output)
                })

                color = Fore.GREEN if status == "completed" else Fore.RED
                print(f"\n{color}✓ Task {status.upper()}: {task.task_description}")
                print(f"{color}   Duration: {task.duration:.2f}s")
                print(f"{color}   Output: {len(output)} characters{Style.RESET_ALL}")
                break

    def track_tool_use(self, agent_name: str, tool_name: str, input_data: str = ""):
        """Track tool usage."""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].tool_calls += 1
            if tool_name not in self.agent_metrics[agent_name].tools_used:
                self.agent_metrics[agent_name].tools_used.append(tool_name)

        # Estimate input tokens
        input_tokens = len(input_data) // 4
        self.input_tokens_estimate += input_tokens
        self.total_tokens_estimate += input_tokens

        self.log_event("tool_use", {
            "agent": agent_name,
            "tool": tool_name,
            "input_length": len(input_data)
        })

        print(f"{Fore.MAGENTA}🔧 Tool Used: {tool_name} by {agent_name}{Style.RESET_ALL}")

    def track_error(self, agent_name: str, error: str):
        """Track an error."""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].errors.append(error)

        self.log_event("error", {
            "agent": agent_name,
            "error": error
        })

        print(f"{Fore.RED}❌ Error in {agent_name}: {error}{Style.RESET_ALL}")

    def finalize(self):
        """Finalize metrics collection."""
        self.end_time = time.time()

    def estimate_cost(self) -> Dict[str, float]:
        """Estimate API costs (rough approximation)."""
        # Rough pricing estimates (as of 2024):
        # GPT-4: $0.03/1K input tokens, $0.06/1K output tokens
        # Claude: $0.015/1K input tokens, $0.075/1K output tokens

        input_cost = (self.input_tokens_estimate / 1000) * 0.03
        output_cost = (self.output_tokens_estimate / 1000) * 0.06
        total_cost = input_cost + output_cost

        return {
            "input_tokens": self.input_tokens_estimate,
            "output_tokens": self.output_tokens_estimate,
            "total_tokens": self.total_tokens_estimate,
            "estimated_cost_usd": round(total_cost, 4),
            "input_cost_usd": round(input_cost, 4),
            "output_cost_usd": round(output_cost, 4)
        }

    def print_summary(self):
        """Print a comprehensive summary of the execution."""
        self.finalize()

        total_time = self.end_time - self.start_time

        print(f"\n\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}📊 AGENT OBSERVABILITY SUMMARY")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

        # Overall metrics
        print(f"{Fore.GREEN}⏱️  Total Execution Time: {total_time:.2f} seconds{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📝 Total Tasks: {len(self.task_metrics)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🤖 Total Agents: {len(self.agent_metrics)}{Style.RESET_ALL}\n")

        # Agent breakdown
        print(f"{Fore.YELLOW}{'─'*70}")
        print(f"{Fore.YELLOW}🤖 AGENT BREAKDOWN")
        print(f"{Fore.YELLOW}{'─'*70}{Style.RESET_ALL}\n")

        for agent_name, metrics in self.agent_metrics.items():
            print(f"{Fore.CYAN}Agent: {agent_name}{Style.RESET_ALL}")
            print(f"  • Time: {metrics.total_time:.2f}s")
            print(f"  • Tool Calls: {metrics.tool_calls}")
            print(f"  • Tools Used: {', '.join(metrics.tools_used) if metrics.tools_used else 'None'}")
            if metrics.errors:
                print(f"  • Errors: {len(metrics.errors)}")
            print()

        # Task breakdown
        print(f"{Fore.YELLOW}{'─'*70}")
        print(f"{Fore.YELLOW}📋 TASK BREAKDOWN")
        print(f"{Fore.YELLOW}{'─'*70}{Style.RESET_ALL}\n")

        for i, task in enumerate(self.task_metrics, 1):
            status_color = Fore.GREEN if task.status == "completed" else Fore.RED
            print(f"{Fore.CYAN}Task {i}: {task.task_description}{Style.RESET_ALL}")
            print(f"  • Agent: {task.agent_name}")
            print(f"  • Status: {status_color}{task.status}{Style.RESET_ALL}")
            print(f"  • Duration: {task.duration:.2f}s")
            print(f"  • Output Length: {task.output_length} characters")
            print()

        # Token and cost estimates
        cost_info = self.estimate_cost()
        print(f"{Fore.YELLOW}{'─'*70}")
        print(f"{Fore.YELLOW}💰 TOKEN USAGE & COST ESTIMATES")
        print(f"{Fore.YELLOW}{'─'*70}{Style.RESET_ALL}\n")

        print(f"  • Input Tokens (est.): {cost_info['input_tokens']:,}")
        print(f"  • Output Tokens (est.): {cost_info['output_tokens']:,}")
        print(f"  • Total Tokens (est.): {cost_info['total_tokens']:,}")
        print(f"  • Estimated Cost: ${cost_info['estimated_cost_usd']:.4f} USD")
        print(f"    - Input Cost: ${cost_info['input_cost_usd']:.4f}")
        print(f"    - Output Cost: ${cost_info['output_cost_usd']:.4f}")

        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

    def export_metrics(self, filepath: str = "crew_metrics.json"):
        """Export all metrics to a JSON file."""
        data = {
            "execution_summary": {
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
                "total_duration": self.end_time - self.start_time if self.end_time else None,
            },
            "agents": {name: metrics.to_dict() for name, metrics in self.agent_metrics.items()},
            "tasks": [task.to_dict() for task in self.task_metrics],
            "cost_estimate": self.estimate_cost(),
            "events": self.events
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"{Fore.GREEN}✓ Metrics exported to {filepath}{Style.RESET_ALL}")
