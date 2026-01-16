"""
Adaptive System - Past moeilijkheidsgraad aan op basis van leerling prestaties.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StudentProgress:
    """Voortgang van een individuele leerling."""
    student_id: str
    groep: int
    results: Dict[str, List[bool]] = field(default_factory=dict)  # prompt_id -> [correct bools]
    current_niveau: Dict[str, int] = field(default_factory=dict)  # domein -> niveau


@dataclass
class ResultRecord:
    """Registratie van een enkel resultaat."""
    student_id: str
    prompt_id: str
    correct: bool
    timestamp: datetime


class AdaptiveSystem:
    """
    Adaptief systeem dat moeilijkheidsgraad aanpast op basis van prestaties.
    """

    def __init__(self):
        """Initialiseer het adaptieve systeem."""
        self.students: Dict[str, StudentProgress] = {}
        self.results: List[ResultRecord] = []

    def record_result(
        self,
        student_id: str,
        prompt_id: str,
        correct: bool
    ) -> None:
        """
        Registreer een resultaat van een leerling.

        Args:
            student_id: Unieke identifier van de leerling.
            prompt_id: ID van de gebruikte prompt.
            correct: Of het antwoord correct was.
        """
        # Voeg toe aan results history
        record = ResultRecord(
            student_id=student_id,
            prompt_id=prompt_id,
            correct=correct,
            timestamp=datetime.now()
        )
        self.results.append(record)

        # Update student progress
        if student_id not in self.students:
            self.students[student_id] = StudentProgress(
                student_id=student_id,
                groep=3  # Default, zou uit database moeten komen
            )

        student = self.students[student_id]
        if prompt_id not in student.results:
            student.results[prompt_id] = []
        student.results[prompt_id].append(correct)

    def get_next_prompt(
        self,
        student_id: str,
        domein: str,
        prompt_library
    ) -> str:
        """
        Bepaal de volgende prompt voor een leerling.

        Args:
            student_id: Unieke identifier van de leerling.
            domein: Rekendomein.
            prompt_library: PromptLibrary instantie voor het zoeken van prompts.

        Returns:
            ID van de geselecteerde prompt.
        """
        if student_id not in self.students:
            # Nieuwe leerling, start met niveau 1
            prompts = prompt_library.search_prompts(
                domein=domein,
                niveau=1
            )
            return prompts[0].id if prompts else None

        student = self.students[student_id]
        current_niveau = student.current_niveau.get(domein, 1)

        # Bereken succes rate voor recent werk
        recent_success = self._calculate_recent_success(student_id, domein)

        # Pas niveau aan op basis van prestatie
        if recent_success > 0.8 and current_niveau < 3:
            # Goed, niveau omhoog
            target_niveau = current_niveau + 1
        elif recent_success < 0.5 and current_niveau > 1:
            # Moeilijk, niveau omlaag
            target_niveau = current_niveau - 1
        else:
            # Blijf op huidig niveau
            target_niveau = current_niveau

        # Update student niveau
        student.current_niveau[domein] = target_niveau

        # Zoek passende prompt
        prompts = prompt_library.search_prompts(
            groep=student.groep,
            domein=domein,
            niveau=target_niveau
        )

        return prompts[0].id if prompts else None

    def _calculate_recent_success(
        self,
        student_id: str,
        domein: str,
        n_recent: int = 10
    ) -> float:
        """
        Bereken succes rate voor recente opdrachten.

        Args:
            student_id: Unieke identifier van de leerling.
            domein: Rekendomein.
            n_recent: Aantal recente opdrachten om te beschouwen.

        Returns:
            Success rate tussen 0 en 1.
        """
        # Filter recente results voor deze student en domein
        student_results = [
            r for r in self.results[-n_recent:]
            if r.student_id == student_id
            # TODO: filter op domein (vereist prompt info in record)
        ]

        if not student_results:
            return 0.5  # Neutral default

        correct_count = sum(1 for r in student_results if r.correct)
        return correct_count / len(student_results)

    def get_student_statistics(self, student_id: str) -> Dict:
        """
        Haal statistieken op voor een leerling.

        Args:
            student_id: Unieke identifier van de leerling.

        Returns:
            Dictionary met statistieken.
        """
        if student_id not in self.students:
            return {}

        student = self.students[student_id]
        student_results = [r for r in self.results if r.student_id == student_id]

        total_opgaven = len(student_results)
        total_correct = sum(1 for r in student_results if r.correct)

        return {
            "student_id": student_id,
            "groep": student.groep,
            "totaal_opgaven": total_opgaven,
            "totaal_correct": total_correct,
            "success_rate": total_correct / total_opgaven if total_opgaven > 0 else 0,
            "huidige_niveaus": student.current_niveau,
        }
