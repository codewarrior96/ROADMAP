from __future__ import annotations

import os
from typing import Dict, List, Any

from dotenv import load_dotenv

from .algorithm import GapAnalysisResult, SkillGap
from .planner import WeekPlan
from .data_loader import Role


def _summarize_priority_reasons(gaps: List[SkillGap]) -> str:
    if not gaps:
        return "Seçtiğiniz rol için ek olarak geliştirmeniz gereken belirgin bir beceri boşluğu bulunmuyor."

    top = gaps[:4]
    parts = []
    order_note_added = False
    for index, gap in enumerate(top, start=1):
        reason_bits = []
        if gap.quick_win:
            reason_bits.append("hızlı motivasyon sağlayan bir başlangıç konusu")
        if gap.difficulty >= 4:
            reason_bits.append("zorluk seviyesi yüksek ama rol için kritik bir beceri")
        if gap.role_weight >= 1.2:
            reason_bits.append("hedef rolünüz için yüksek ağırlığa sahip")

        level_info = (
            f"mevcut seviyeniz **{gap.current_level}**, hedef seviye ise **{gap.required_level}** olduğu için "
            f"aradaki boşluk **{gap.gap} seviye**."
        )

        reason_txt = "; ".join(reason_bits) if reason_bits else "hedef rolünüzde doğrudan iş çıktısına etki eden"
        parts.append(
            f"{index}. sırada **{gap.display_name}** yer alıyor; çünkü {reason_txt} ve {level_info}"
        )

        if gap.missing_prerequisites and not order_note_added:
            order_note_added = True
            parts.append(
                "Bu sıralamada, eksik önkoşulları olan beceriler mümkün olduğunca daha geç haftalara yerleştirilirken, "
                "önce onları destekleyen temel konulara odaklanılır."
            )

    parts.append(
        "Genel olarak sistem, önce önkoşul ve temel konuları, ardından rol ağırlığı yüksek ve seviye boşluğu fazla olan "
        "becerileri öne alarak, öğrenme yükünü haftalara yayılmış şekilde dengeler."
    )

    return "\n\n".join(parts)


def _summarize_expected_gains(role: Role, weeks: List[WeekPlan]) -> str:
    focused_skills = {s.skill_id for w in weeks for s in w.skills}
    total_weeks = len(weeks)
    if not focused_skills:
        return (
            "Seçtiğiniz süre ve haftalık çalışma sınırları içinde ek bir beceri planı oluşturulmadı; "
            "önce rol ve beceri boşluklarını tekrar gözden geçirmeniz önerilir."
        )

    return (
        f"Bu {total_weeks} haftalık plan sonunda **{role.display_name}** rolüne bir adım daha yaklaşıp, "
        f"özellikle odaklandığınız {len(focused_skills)} temel beceri üzerinde uygulamalı deneyim kazanmanız beklenir. "
        "Her hafta seçilen 1-2 odak beceri sayesinde hem temel kavramlarda hem de küçük uygulamalarda ilerleyerek, "
        "gerçek projelere daha hazır ve özgüvenli bir seviyeye gelmeniz hedeflenir."
    )


def generate_deterministic_explanation(
    role: Role,
    gap_result: GapAnalysisResult,
    weeks: List[WeekPlan],
) -> Dict[str, str]:
    """Always-available local explanation in Turkish."""
    gaps = gap_result.skill_gaps

    total_weeks = len(weeks)

    if not gaps:
        short = (
            f"Şu an için **{role.display_name}** rolü açısından büyük bir beceri boşluğunuz görünmüyor. "
            f"Bu nedenle sistem, {total_weeks} haftalık yeni bir yoğun öğrenme planı önermek yerine mevcut seviyenizi korumanızı ve "
            "küçük geliştirmeler yapmanızı tavsiye ediyor."
        )
        return {
            "short_summary": short,
            "priority_rationale": "Belirgin bir beceri boşluğu bulunmadığı için ayrıntılı bir önceliklendirme yapılmadı.",
            "expected_gains": _summarize_expected_gains(role, weeks),
        }

    first = gaps[0]
    total_missing = len(gaps)
    short = (
        f"Sistem, **{role.display_name}** rolüne yaklaşmanız için üzerinde özellikle çalışmanız gereken "
        f"{total_missing} ana beceri boşluğu tespit etti. "
        f"İlk odak alanlarından biri **{first.display_name}**, çünkü mevcut seviyeniz ({first.current_level}) ile "
        f"hedef seviye ({first.required_level}) arasında belirgin bir fark bulunuyor."
    )

    priority_text = _summarize_priority_reasons(gaps)
    gains_text = _summarize_expected_gains(role, weeks)

    return {
        "short_summary": short,
        "priority_rationale": priority_text,
        "expected_gains": gains_text,
    }


def generate_explanation_with_llm(
    role: Role,
    gap_result: GapAnalysisResult,
    weeks: List[WeekPlan],
) -> Dict[str, str]:
    """
    Optional enhanced layer using OpenAI if OPENAI_API_KEY exists.
    If anything goes wrong, falls back to deterministic mode.
    """
    load_dotenv(override=False)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return generate_deterministic_explanation(role, gap_result, weeks)

    try:
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=api_key)

        # Küçük, maliyeti düşük ve Türkçe odaklı bir açıklama promptu
        roadmap_brief = []
        for w in weeks:
            if not w.skills:
                continue
            skills_txt = ", ".join(s.display_name for s in w.skills)
            roadmap_brief.append(f"{w.week_index}. hafta: {skills_txt}")

        gaps_brief = []
        for g in gap_result.skill_gaps[:6]:
            gaps_brief.append(
                f"{g.display_name} (mevcut: {g.current_level}, hedef: {g.required_level}, boşluk: {g.gap}, skor: {g.priority_score:.2f})"
            )

        system_prompt = (
            "Sen üniversite seviyesinde bir yapay zeka öğrenme koçusun. "
            "Kullanıcıya sade, motive edici ve net Türkçe açıklamalar yaparsın. "
            "Cevaplarını mutlaka üç bölüm halinde yaz: kısa özet, öncelik mantığı, 4 hafta sonu kazanımlar."
        )

        user_prompt = (
            f"Hedef rol: {role.display_name}\n\n"
            f"Öncelikli beceri boşlukları:\n- " + "\n- ".join(gaps_brief) + "\n\n"
            "4 haftalık plan özeti:\n- " + "\n- ".join(roadmap_brief) + "\n\n"
            "Bu bilgilerden yola çıkarak, kullanıcının neden bu sırayla ilerlediğini ve "
            "4 hafta sonunda neler kazanabileceğini açıkla."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )

        content = response.choices[0].message.content or ""
        # Çok basit bir bölme: beklenen başlıklara göre ayıramazsak, tamamını kısa özet olarak kabul ederiz.
        # Burada sadece tek string döndürmek yerine üç alanı kaba bir şekilde dolduruyoruz.
        return {
            "short_summary": content,
            "priority_rationale": "Bu açıklama, OpenAI tabanlı geliştirilmiş moddan üretildi.",
            "expected_gains": "Detaylı kazanım açıklaması yukarıdaki metin içinde yer almaktadır.",
        }
    except Exception:
        # Her türlü hata durumda sessizce deterministik moda geri dön.
        return generate_deterministic_explanation(role, gap_result, weeks)

