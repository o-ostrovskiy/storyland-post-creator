"""Agent evaluation system for assessing content quality and performance."""
import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import textstat
from colorama import Fore, Style


@dataclass
class ContentQualityScore:
    """Content quality assessment scores."""
    readability_score: float  # 0-100
    structure_score: float  # 0-100
    seo_score: float  # 0-100
    completeness_score: float  # 0-100
    overall_score: float  # 0-100
    grade: str  # A, B, C, D, F
    issues: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class AgentPerformanceScore:
    """Agent performance assessment scores."""
    efficiency_score: float  # 0-100
    reliability_score: float  # 0-100
    quality_score: float  # 0-100
    overall_score: float  # 0-100
    grade: str  # A, B, C, D, F
    strengths: List[str]
    weaknesses: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class ContentEvaluator:
    """Evaluates blog post content quality."""

    def __init__(self):
        """Initialize the evaluator."""
        self.min_word_count = 800
        self.max_word_count = 1500
        self.target_reading_ease = 60  # Flesch Reading Ease target

    def evaluate_content(
        self,
        title: str,
        content: str,
        tags: str
    ) -> ContentQualityScore:
        """
        Evaluate blog post content quality.

        Args:
            title: Blog post title
            content: HTML content
            tags: Comma-separated tags

        Returns:
            ContentQualityScore with detailed assessment
        """
        issues = []
        recommendations = []

        # Parse HTML
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        word_count = len(text.split())

        # 1. Readability Score (0-100)
        readability_score = self._evaluate_readability(text, issues, recommendations)

        # 2. Structure Score (0-100)
        structure_score = self._evaluate_structure(soup, content, issues, recommendations)

        # 3. SEO Score (0-100)
        seo_score = self._evaluate_seo(title, content, tags, word_count, issues, recommendations)

        # 4. Completeness Score (0-100)
        completeness_score = self._evaluate_completeness(
            title, content, tags, word_count, soup, issues, recommendations
        )

        # Calculate overall score (weighted average)
        overall_score = (
            readability_score * 0.25 +
            structure_score * 0.25 +
            seo_score * 0.25 +
            completeness_score * 0.25
        )

        # Assign grade
        grade = self._score_to_grade(overall_score)

        return ContentQualityScore(
            readability_score=round(readability_score, 2),
            structure_score=round(structure_score, 2),
            seo_score=round(seo_score, 2),
            completeness_score=round(completeness_score, 2),
            overall_score=round(overall_score, 2),
            grade=grade,
            issues=issues,
            recommendations=recommendations
        )

    def _evaluate_readability(
        self,
        text: str,
        issues: List[str],
        recommendations: List[str]
    ) -> float:
        """Evaluate content readability."""
        score = 100.0

        try:
            # Flesch Reading Ease (0-100, higher is easier)
            reading_ease = textstat.flesch_reading_ease(text)

            # Flesch-Kincaid Grade Level
            grade_level = textstat.flesch_kincaid_grade(text)

            # Check reading ease
            if reading_ease < 50:
                issues.append(f"Content is difficult to read (score: {reading_ease:.1f})")
                recommendations.append("Use shorter sentences and simpler words")
                score -= 20
            elif reading_ease < 60:
                recommendations.append("Could improve readability with simpler language")
                score -= 10

            # Check grade level (target: 8-10th grade)
            if grade_level > 12:
                issues.append(f"Content requires college-level reading (grade {grade_level:.1f})")
                recommendations.append("Simplify complex sentences")
                score -= 15
            elif grade_level < 6:
                issues.append("Content may be too simplistic")
                score -= 5

            # Average sentence length
            avg_sentence_length = textstat.avg_sentence_length(text)
            if avg_sentence_length > 25:
                recommendations.append("Consider breaking up long sentences")
                score -= 10

        except Exception as e:
            issues.append(f"Could not fully assess readability: {str(e)}")
            score = 75

        return max(0, score)

    def _evaluate_structure(
        self,
        soup: BeautifulSoup,
        content: str,
        issues: List[str],
        recommendations: List[str]
    ) -> float:
        """Evaluate content structure."""
        score = 100.0

        # Check for H2 tags (main sections)
        h2_tags = soup.find_all('h2')
        if len(h2_tags) < 3:
            issues.append(f"Only {len(h2_tags)} main sections (H2). Need at least 3")
            recommendations.append("Add more main sections with H2 headings")
            score -= 25
        elif len(h2_tags) > 8:
            issues.append("Too many main sections - content may be fragmented")
            score -= 10

        # Check for H3 tags (subsections)
        h3_tags = soup.find_all('h3')
        if len(h3_tags) == 0:
            recommendations.append("Consider adding subsections with H3 headings")
            score -= 10

        # Check for paragraphs
        p_tags = soup.find_all('p')
        if len(p_tags) < 5:
            issues.append("Too few paragraphs - content lacks depth")
            recommendations.append("Break content into more paragraphs")
            score -= 20

        # Check for lists (ul/ol)
        lists = soup.find_all(['ul', 'ol'])
        if len(lists) == 0:
            recommendations.append("Consider using bullet points or numbered lists")
            score -= 10

        # Check for proper HTML formatting
        if '<h1>' in content.lower():
            issues.append("Contains H1 tag - title should be separate")
            score -= 15

        # Check for strong/em tags (emphasis)
        strong_tags = soup.find_all(['strong', 'em', 'b', 'i'])
        if len(strong_tags) == 0:
            recommendations.append("Add emphasis to key points using bold/italic")
            score -= 5

        return max(0, score)

    def _evaluate_seo(
        self,
        title: str,
        content: str,
        tags: str,
        word_count: int,
        issues: List[str],
        recommendations: List[str]
    ) -> float:
        """Evaluate SEO compliance."""
        score = 100.0

        # Title length (50-70 characters is ideal)
        title_len = len(title)
        if title_len < 30:
            issues.append(f"Title too short ({title_len} chars). SEO optimal: 50-70")
            recommendations.append("Expand title to 50-70 characters")
            score -= 20
        elif title_len < 50:
            recommendations.append("Title could be longer for better SEO")
            score -= 10
        elif title_len > 70:
            issues.append(f"Title too long ({title_len} chars). May be truncated")
            recommendations.append("Shorten title to 50-70 characters")
            score -= 15

        # Tag count (3-5 is ideal)
        tag_list = [t.strip() for t in tags.split(',') if t.strip()]
        if len(tag_list) < 3:
            issues.append(f"Only {len(tag_list)} tags. Recommended: 3-5")
            recommendations.append("Add more relevant tags")
            score -= 15
        elif len(tag_list) > 7:
            issues.append("Too many tags - dilutes focus")
            recommendations.append("Reduce to 3-5 most relevant tags")
            score -= 10

        # Word count (800-1500 for blog posts)
        if word_count < 800:
            issues.append(f"Content too short ({word_count} words). Target: 800-1500")
            recommendations.append("Expand content with more details and examples")
            score -= 25
        elif word_count > 2000:
            recommendations.append("Content is quite long - consider breaking into series")
            score -= 5

        # Keyword density (title keywords should appear in content)
        title_words = set(re.findall(r'\w+', title.lower()))
        content_lower = content.lower()
        keyword_appearances = sum(1 for word in title_words if len(word) > 4 and word in content_lower)

        if keyword_appearances < 2:
            issues.append("Title keywords barely appear in content")
            recommendations.append("Use title keywords naturally throughout content")
            score -= 20

        return max(0, score)

    def _evaluate_completeness(
        self,
        title: str,
        content: str,
        tags: str,
        word_count: int,
        soup: BeautifulSoup,
        issues: List[str],
        recommendations: List[str]
    ) -> float:
        """Evaluate content completeness."""
        score = 100.0

        # Check for introduction
        p_tags = soup.find_all('p')
        if p_tags:
            first_para = p_tags[0].get_text()
            if len(first_para.split()) < 30:
                issues.append("Introduction paragraph is too short")
                recommendations.append("Expand introduction to engage readers")
                score -= 15

        # Check for conclusion
        if p_tags:
            last_para = p_tags[-1].get_text()
            conclusion_words = ['conclusion', 'summary', 'in closing', 'to wrap up', 'finally']
            has_conclusion = any(word in last_para.lower() for word in conclusion_words)

            if not has_conclusion and len(last_para.split()) < 30:
                recommendations.append("Consider adding a clear conclusion")
                score -= 10

        # Check content depth (multiple paragraphs per section)
        h2_count = len(soup.find_all('h2'))
        p_count = len(p_tags)

        if h2_count > 0:
            avg_paras_per_section = p_count / h2_count
            if avg_paras_per_section < 2:
                issues.append("Sections lack depth - need more content per section")
                recommendations.append("Expand each section with more details")
                score -= 20

        # Check for empty or placeholder content
        placeholder_words = ['lorem ipsum', 'placeholder', 'todo', 'tbd', 'xxx']
        if any(word in content.lower() for word in placeholder_words):
            issues.append("Content contains placeholder text")
            score -= 30

        # Check minimum viable content
        if word_count < 500:
            issues.append("Content critically short - not viable for publication")
            score -= 40

        return max(0, score)

    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"


class AgentEvaluator:
    """Evaluates agent performance."""

    def __init__(self):
        """Initialize the evaluator."""
        pass

    def evaluate_agent_performance(
        self,
        agent_metrics: Dict[str, Any],
        task_metrics: List[Dict[str, Any]],
        total_duration: float
    ) -> AgentPerformanceScore:
        """
        Evaluate overall agent performance.

        Args:
            agent_metrics: Dictionary of agent metrics
            task_metrics: List of task metrics
            total_duration: Total execution time

        Returns:
            AgentPerformanceScore with assessment
        """
        strengths = []
        weaknesses = []

        # 1. Efficiency Score (speed and resource usage)
        efficiency_score = self._evaluate_efficiency(
            agent_metrics, task_metrics, total_duration, strengths, weaknesses
        )

        # 2. Reliability Score (error rates, completion)
        reliability_score = self._evaluate_reliability(
            agent_metrics, task_metrics, strengths, weaknesses
        )

        # 3. Quality Score (based on output quality)
        quality_score = self._evaluate_quality(
            task_metrics, strengths, weaknesses
        )

        # Calculate overall score
        overall_score = (
            efficiency_score * 0.30 +
            reliability_score * 0.35 +
            quality_score * 0.35
        )

        grade = self._score_to_grade(overall_score)

        return AgentPerformanceScore(
            efficiency_score=round(efficiency_score, 2),
            reliability_score=round(reliability_score, 2),
            quality_score=round(quality_score, 2),
            overall_score=round(overall_score, 2),
            grade=grade,
            strengths=strengths,
            weaknesses=weaknesses
        )

    def _evaluate_efficiency(
        self,
        agent_metrics: Dict[str, Any],
        task_metrics: List[Dict[str, Any]],
        total_duration: float,
        strengths: List[str],
        weaknesses: List[str]
    ) -> float:
        """Evaluate agent efficiency."""
        score = 100.0

        # Check total duration (target: under 60 seconds)
        if total_duration < 30:
            strengths.append(f"Very fast execution ({total_duration:.1f}s)")
        elif total_duration > 90:
            weaknesses.append(f"Slow execution ({total_duration:.1f}s)")
            score -= 25
        elif total_duration > 60:
            weaknesses.append("Execution time above target")
            score -= 15

        # Check tool usage efficiency
        total_tool_calls = sum(
            metrics.get('tool_calls', 0)
            for metrics in agent_metrics.values()
        )

        if total_tool_calls > 10:
            weaknesses.append(f"High tool usage ({total_tool_calls} calls)")
            score -= 15
        elif total_tool_calls < 3:
            weaknesses.append("Very few tool calls - may lack thoroughness")
            score -= 10

        # Check task completion times
        slow_tasks = [t for t in task_metrics if t.get('duration', 0) > 30]
        if slow_tasks:
            weaknesses.append(f"{len(slow_tasks)} slow tasks detected")
            score -= 10 * len(slow_tasks)

        return max(0, score)

    def _evaluate_reliability(
        self,
        agent_metrics: Dict[str, Any],
        task_metrics: List[Dict[str, Any]],
        strengths: List[str],
        weaknesses: List[str]
    ) -> float:
        """Evaluate agent reliability."""
        score = 100.0

        # Check for errors
        total_errors = sum(
            len(metrics.get('errors', []))
            for metrics in agent_metrics.values()
        )

        if total_errors == 0:
            strengths.append("Zero errors during execution")
        else:
            weaknesses.append(f"{total_errors} errors occurred")
            score -= 20 * total_errors

        # Check task completion
        failed_tasks = [t for t in task_metrics if t.get('status') != 'completed']
        if failed_tasks:
            weaknesses.append(f"{len(failed_tasks)} tasks failed")
            score -= 30 * len(failed_tasks)
        else:
            strengths.append("All tasks completed successfully")

        # Check for consistency (similar tasks should take similar time)
        durations = [t.get('duration', 0) for t in task_metrics if t.get('duration', 0) > 0]
        if durations:
            avg_duration = sum(durations) / len(durations)
            variance = sum((d - avg_duration) ** 2 for d in durations) / len(durations)

            if variance > 100:
                weaknesses.append("Inconsistent task completion times")
                score -= 10

        return max(0, score)

    def _evaluate_quality(
        self,
        task_metrics: List[Dict[str, Any]],
        strengths: List[str],
        weaknesses: List[str]
    ) -> float:
        """Evaluate output quality."""
        score = 100.0

        # Check output lengths
        for task in task_metrics:
            output_len = task.get('output_length', 0)

            # Very short outputs may indicate issues
            if output_len > 0 and output_len < 50:
                weaknesses.append(f"Task produced very short output ({output_len} chars)")
                score -= 15

        # Check for substantive outputs
        substantial_outputs = [t for t in task_metrics if t.get('output_length', 0) > 500]
        if substantial_outputs:
            strengths.append(f"{len(substantial_outputs)} tasks with substantial output")

        return max(0, score)

    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"


class EvaluationReporter:
    """Generates evaluation reports."""

    @staticmethod
    def print_content_evaluation(evaluation: ContentQualityScore):
        """Print content quality evaluation."""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}📝 CONTENT QUALITY EVALUATION")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

        # Overall score
        grade_color = EvaluationReporter._grade_color(evaluation.grade)
        print(f"{grade_color}Overall Score: {evaluation.overall_score}/100 (Grade: {evaluation.grade}){Style.RESET_ALL}\n")

        # Individual scores
        print(f"{Fore.YELLOW}Detailed Scores:{Style.RESET_ALL}")
        print(f"  • Readability: {evaluation.readability_score}/100")
        print(f"  • Structure: {evaluation.structure_score}/100")
        print(f"  • SEO: {evaluation.seo_score}/100")
        print(f"  • Completeness: {evaluation.completeness_score}/100\n")

        # Issues
        if evaluation.issues:
            print(f"{Fore.RED}⚠️  Issues Found ({len(evaluation.issues)}):{Style.RESET_ALL}")
            for issue in evaluation.issues:
                print(f"  • {issue}")
            print()

        # Recommendations
        if evaluation.recommendations:
            print(f"{Fore.YELLOW}💡 Recommendations ({len(evaluation.recommendations)}):{Style.RESET_ALL}")
            for rec in evaluation.recommendations:
                print(f"  • {rec}")
            print()

        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

    @staticmethod
    def print_agent_evaluation(evaluation: AgentPerformanceScore):
        """Print agent performance evaluation."""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}🤖 AGENT PERFORMANCE EVALUATION")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

        # Overall score
        grade_color = EvaluationReporter._grade_color(evaluation.grade)
        print(f"{grade_color}Overall Score: {evaluation.overall_score}/100 (Grade: {evaluation.grade}){Style.RESET_ALL}\n")

        # Individual scores
        print(f"{Fore.YELLOW}Detailed Scores:{Style.RESET_ALL}")
        print(f"  • Efficiency: {evaluation.efficiency_score}/100")
        print(f"  • Reliability: {evaluation.reliability_score}/100")
        print(f"  • Quality: {evaluation.quality_score}/100\n")

        # Strengths
        if evaluation.strengths:
            print(f"{Fore.GREEN}✓ Strengths ({len(evaluation.strengths)}):{Style.RESET_ALL}")
            for strength in evaluation.strengths:
                print(f"  • {strength}")
            print()

        # Weaknesses
        if evaluation.weaknesses:
            print(f"{Fore.RED}✗ Areas for Improvement ({len(evaluation.weaknesses)}):{Style.RESET_ALL}")
            for weakness in evaluation.weaknesses:
                print(f"  • {weakness}")
            print()

        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

    @staticmethod
    def export_evaluation(
        content_eval: ContentQualityScore,
        agent_eval: AgentPerformanceScore,
        filepath: str = "evaluation_report.json"
    ):
        """Export evaluation to JSON."""
        data = {
            "content_quality": content_eval.to_dict(),
            "agent_performance": agent_eval.to_dict(),
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"{Fore.GREEN}✓ Evaluation report exported to {filepath}{Style.RESET_ALL}")

    @staticmethod
    def _grade_color(grade: str) -> str:
        """Get color for grade."""
        if grade == "A":
            return Fore.GREEN
        elif grade == "B":
            return Fore.CYAN
        elif grade == "C":
            return Fore.YELLOW
        else:
            return Fore.RED
