"""
Prompt Library - Beheer en laden van prompt bestanden.

Deze module biedt de kernfunctionaliteit voor het laden, beheren en
doorzoeken van AI prompts voor het genereren van rekenopdrachten.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


class PromptLibrary:
    """Centrale bibliotheek voor het beheren van prompts."""

    def __init__(self, prompts_path: Optional[Path] = None):
        """
        Initialiseer de prompt library.

        Args:
            prompts_path: Pad naar de prompts directory. Indien None,
                         wordt de standaard 'prompts/' directory gebruikt.
        """
        self.prompts_path = prompts_path or Path(__file__).parent.parent / "prompts"
        self.prompts: Dict[str, Dict] = {}

    def load_prompts(self, path: Optional[Path] = None) -> None:
        """
        Laad alle prompts uit een directory.

        Args:
            path: Pad naar de prompts directory. Gebruikt self.prompts_path indien None.

        Raises:
            FileNotFoundError: Als de prompts directory niet bestaat.
            yaml.YAMLError: Als een prompt bestand geen valide YAML is.
        """
        load_path = path or self.prompts_path

        if not load_path.exists():
            raise FileNotFoundError(f"Prompts directory niet gevonden: {load_path}")

        # Laad alle YAML bestanden recursief
        for yaml_file in load_path.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'PROMPT_ID' in data:
                        prompt_id = data['PROMPT_ID']
                        self.prompts[prompt_id] = data
                        print(f"✓ Geladen: {prompt_id}")
                    else:
                        print(f"⚠ Overgeslagen (geen PROMPT_ID): {yaml_file}")
            except yaml.YAMLError as e:
                print(f"✗ Fout bij laden {yaml_file}: {e}")
            except Exception as e:
                print(f"✗ Onverwachte fout bij {yaml_file}: {e}")

        print(f"\n📚 Totaal {len(self.prompts)} prompts geladen")

    def get_prompt(self, prompt_id: str) -> Dict:
        """
        Haal een specifieke prompt op.

        Args:
            prompt_id: Unieke identifier van de prompt (bijv. "G5_GB_N2_001").

        Returns:
            Dict met de volledige prompt data.

        Raises:
            KeyError: Als de prompt niet bestaat.
        """
        if prompt_id not in self.prompts:
            raise KeyError(f"Prompt niet gevonden: {prompt_id}")
        return self.prompts[prompt_id]

    def search_prompts(
        self,
        groep: Optional[int] = None,
        inhoudslijn: Optional[str] = None,
        niveau: Optional[str] = None,
    ) -> List[Dict]:
        """
        Zoek prompts op basis van criteria.

        Args:
            groep: Groep nummer (3-8).
            inhoudslijn: Inhoudslijn (Getalbegrip, Strategieën, Bewerkingen,
                        Schriftelijk rekenen).
            niveau: Niveau (N1, N2, N3, N4).

        Returns:
            Lijst van matchende prompts.
        """
        results = list(self.prompts.values())

        if groep is not None:
            results = [p for p in results
                      if p.get('METADATA', {}).get('groep') == groep]

        if inhoudslijn is not None:
            results = [p for p in results
                      if p.get('METADATA', {}).get('inhoudslijn', '').lower() == inhoudslijn.lower()]

        if niveau is not None:
            results = [p for p in results
                      if p.get('METADATA', {}).get('niveau', '').upper() == niveau.upper()]

        return results

    def get_prompts_for_level(
        self,
        groep: int,
        inhoudslijn: str,
        niveau: str
    ) -> List[Dict]:
        """
        Haal alle prompts voor een specifiek niveau.

        Args:
            groep: Groep nummer (3-8).
            inhoudslijn: Inhoudslijn.
            niveau: Niveau (N1-N4).

        Returns:
            Lijst van prompts voor dit niveau.
        """
        return self.search_prompts(groep=groep, inhoudslijn=inhoudslijn, niveau=niveau)

    def list_inhoudslijnen(self, groep: Optional[int] = None) -> List[str]:
        """
        Haal een lijst van alle beschikbare inhoudslijnen op.

        Args:
            groep: Optioneel, filter op groep.

        Returns:
            Lijst van unieke inhoudslijn namen.
        """
        prompts = self.search_prompts(groep=groep) if groep else list(self.prompts.values())
        return sorted(set(
            p.get('METADATA', {}).get('inhoudslijn', '')
            for p in prompts
            if p.get('METADATA', {}).get('inhoudslijn')
        ))

    def get_statistics(self) -> Dict:
        """
        Haal statistieken op over de geladen prompts.

        Returns:
            Dict met statistieken (aantal per groep, niveau, etc.).
        """
        stats = {
            'totaal': len(self.prompts),
            'per_groep': {},
            'per_niveau': {},
            'per_inhoudslijn': {}
        }

        for prompt in self.prompts.values():
            metadata = prompt.get('METADATA', {})

            # Per groep
            groep = metadata.get('groep')
            if groep:
                stats['per_groep'][groep] = stats['per_groep'].get(groep, 0) + 1

            # Per niveau
            niveau = metadata.get('niveau')
            if niveau:
                stats['per_niveau'][niveau] = stats['per_niveau'].get(niveau, 0) + 1

            # Per inhoudslijn
            lijn = metadata.get('inhoudslijn')
            if lijn:
                stats['per_inhoudslijn'][lijn] = stats['per_inhoudslijn'].get(lijn, 0) + 1

        return stats

    def __repr__(self) -> str:
        return f"<PromptLibrary: {len(self.prompts)} prompts geladen>"
