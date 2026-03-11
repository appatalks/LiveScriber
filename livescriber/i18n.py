"""UI string translations for LiveScriber localization."""

from __future__ import annotations

# All translatable UI strings keyed by identifier.
# Each language provides its own mapping; missing keys fall back to English.

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "transcribe": "Transcribe",
        "summarize": "Summarize",
        "import_audio": "Import Audio",
        "copy_all": "Copy All",
        "save_md": "Save MD",
        "save_wav": "Save WAV",
        "play": "▶ Play",
        "stop_play": "■ Stop",
        "new_session": "New session",
        "previous_session": "Previous session",
        "next_session": "Next / New session",
        "recording": "Recording…",
        "ready": "Ready",
        "transcribing": "Transcribing… (this may take a moment)",
        "transcription_complete": "Transcription complete",
        "generating_summary": "Generating summary…",
        "summary_ready": "Summary ready",
        "summary_error": "Summary error",
        "no_recording": "No recording to transcribe",
        "no_audio_play": "No audio to play",
        "playing": "Playing…",
        "nothing_to_copy": "Nothing to copy",
        "copied": "Copied to clipboard",
        "nothing_to_save": "Nothing to save",
        "transcription": "Transcription",
        "summary_notes": "Summary && Notes",
        "settings": "Settings",
        "transcribe_first": "Transcribe first before summarizing",
        "mic_error": "Mic error",
        "stop_error": "Stop error",
        "live_active": "[Live transcription active]",
        "live_loading": "Recording… (loading transcription model)",
        "live_win_na": "Recording… (live transcription not available on Windows)",
        "live_ready": "live transcript ready",
        "recorded": "Recorded",
        "session": "session",
        # Settings dialog
        "settings_title": "LiveScriber Settings",
        "grp_transcription": "Transcription",
        "whisper_model": "Whisper model:",
        "language": "Language:",
        "auto_detect": "auto-detect (leave empty)",
        "live_transcription_label": "Live transcription while recording (experimental)",
        "auto_translate_label": "Auto-translate to English",
        "grp_summarization": "Summarization",
        "backend": "Backend:",
        "system_prompt": "System prompt:",
        "grp_audio": "Audio",
        "capture_system_audio": "Capture system audio (speakers)",
        "grp_appearance": "Appearance",
        "theme": "Theme:",
        "always_on_top": "Always on top",
        "opacity": "Opacity:",
        "save_btn": "Save",
        "cancel_btn": "Cancel",
        "about": "About",
    },
    "ko": {
        "transcribe": "텍스트 변환",
        "summarize": "요약",
        "import_audio": "오디오 가져오기",
        "copy_all": "전체 복사",
        "save_md": "MD 저장",
        "save_wav": "WAV 저장",
        "play": "▶ 재생",
        "stop_play": "■ 정지",
        "new_session": "새 세션",
        "previous_session": "이전 세션",
        "next_session": "다음 / 새 세션",
        "recording": "녹음 중…",
        "ready": "준비됨",
        "transcribing": "텍스트 변환 중… (잠시 기다려 주세요)",
        "transcription_complete": "텍스트 변환 완료",
        "generating_summary": "요약 생성 중…",
        "summary_ready": "요약 완료",
        "summary_error": "요약 오류",
        "no_recording": "변환할 녹음이 없습니다",
        "no_audio_play": "재생할 오디오가 없습니다",
        "playing": "재생 중…",
        "nothing_to_copy": "복사할 내용이 없습니다",
        "copied": "클립보드에 복사됨",
        "nothing_to_save": "저장할 내용이 없습니다",
        "transcription": "텍스트 변환",
        "summary_notes": "요약 && 노트",
        "settings": "설정",
        "transcribe_first": "먼저 텍스트 변환을 실행하세요",
        "mic_error": "마이크 오류",
        "stop_error": "중지 오류",
        "live_active": "[실시간 텍스트 변환 활성화]",
        "live_loading": "녹음 중… (변환 모델 로딩 중)",
        "live_win_na": "녹음 중… (Windows에서 실시간 변환 불가)",
        "live_ready": "실시간 변환 완료",
        "recorded": "녹음됨",
        "session": "세션",
        "settings_title": "LiveScriber 설정",
        "grp_transcription": "텍스트 변환",
        "whisper_model": "Whisper 모델:",
        "language": "언어:",
        "auto_detect": "자동 감지 (비워 두세요)",
        "live_transcription_label": "녹음 중 실시간 변환 (실험적)",
        "auto_translate_label": "영어로 자동 번역 (Append English)",
        "grp_summarization": "요약",
        "backend": "백엔드:",
        "system_prompt": "시스템 프롬프트:",
        "grp_audio": "오디오",
        "capture_system_audio": "시스템 오디오 캡처 (스피커)",
        "grp_appearance": "외관",
        "theme": "테마:",
        "always_on_top": "항상 위에",
        "opacity": "투명도:",
        "save_btn": "저장",
        "cancel_btn": "취소",
        "about": "정보",
    },
    "ja": {
        "transcribe": "文字起こし",
        "summarize": "要約",
        "import_audio": "音声を取り込む",
        "copy_all": "すべてコピー",
        "save_md": "MD保存",
        "save_wav": "WAV保存",
        "play": "▶ 再生",
        "stop_play": "■ 停止",
        "new_session": "新しいセッション",
        "previous_session": "前のセッション",
        "next_session": "次 / 新しいセッション",
        "recording": "録音中…",
        "ready": "準備完了",
        "transcribing": "文字起こし中… (少々お待ちください)",
        "transcription_complete": "文字起こし完了",
        "generating_summary": "要約を生成中…",
        "summary_ready": "要約完了",
        "summary_error": "要約エラー",
        "no_recording": "文字起こしする録音がありません",
        "no_audio_play": "再生する音声がありません",
        "playing": "再生中…",
        "nothing_to_copy": "コピーするものがありません",
        "copied": "クリップボードにコピーしました",
        "nothing_to_save": "保存するものがありません",
        "transcription": "文字起こし",
        "summary_notes": "要約 && ノート",
        "settings": "設定",
        "transcribe_first": "先に文字起こしを実行してください",
        "mic_error": "マイクエラー",
        "stop_error": "停止エラー",
        "live_active": "[リアルタイム文字起こし有効]",
        "live_loading": "録音中… (変換モデル読み込み中)",
        "live_win_na": "録音中… (Windowsではリアルタイム変換不可)",
        "live_ready": "リアルタイム変換完了",
        "recorded": "録音済み",
        "session": "セッション",
        "settings_title": "LiveScriber 設定",
        "grp_transcription": "文字起こし",
        "whisper_model": "Whisperモデル:",
        "language": "言語:",
        "auto_detect": "自動検出 (空欄のまま)",
        "live_transcription_label": "録音中のリアルタイム変換 (実験的)",
        "auto_translate_label": "英語に自動翻訳 (Append English)",
        "grp_summarization": "要約",
        "backend": "バックエンド:",
        "system_prompt": "システムプロンプト:",
        "grp_audio": "オーディオ",
        "capture_system_audio": "システム音声をキャプチャ (スピーカー)",
        "grp_appearance": "外観",
        "theme": "テーマ:",
        "always_on_top": "常に前面表示",
        "opacity": "不透明度:",
        "save_btn": "保存",
        "cancel_btn": "キャンセル",
        "about": "概要",
    },
    "uk": {
        "transcribe": "Транскрибувати",
        "summarize": "Підсумок",
        "import_audio": "Імпорт аудіо",
        "copy_all": "Копіювати все",
        "save_md": "Зберегти MD",
        "save_wav": "Зберегти WAV",
        "play": "▶ Відтворити",
        "stop_play": "■ Зупинити",
        "new_session": "Новий сеанс",
        "previous_session": "Попередній сеанс",
        "next_session": "Наступний / Новий сеанс",
        "recording": "Запис…",
        "ready": "Готово",
        "transcribing": "Транскрибування… (зачекайте)",
        "transcription_complete": "Транскрибування завершено",
        "generating_summary": "Створення підсумку…",
        "summary_ready": "Підсумок готовий",
        "summary_error": "Помилка підсумку",
        "no_recording": "Немає запису для транскрибування",
        "no_audio_play": "Немає аудіо для відтворення",
        "playing": "Відтворення…",
        "nothing_to_copy": "Нічого копіювати",
        "copied": "Скопійовано в буфер обміну",
        "nothing_to_save": "Нічого зберігати",
        "transcription": "Транскрипція",
        "summary_notes": "Підсумок && Нотатки",
        "settings": "Налаштування",
        "transcribe_first": "Спочатку транскрибуйте",
        "mic_error": "Помилка мікрофона",
        "stop_error": "Помилка зупинки",
        "live_active": "[Живе транскрибування активне]",
        "live_loading": "Запис… (завантаження моделі)",
        "live_win_na": "Запис… (живе транскрибування недоступне на Windows)",
        "live_ready": "живий транскрипт готовий",
        "recorded": "Записано",
        "session": "сеанс",
        "settings_title": "LiveScriber Налаштування",
        "grp_transcription": "Транскрипція",
        "whisper_model": "Модель Whisper:",
        "language": "Мова:",
        "auto_detect": "автовизначення (залиште порожнім)",
        "live_transcription_label": "Живе транскрибування під час запису (експ.)",
        "auto_translate_label": "Автопереклад англійською (Append English)",
        "grp_summarization": "Підсумок",
        "backend": "Бекенд:",
        "system_prompt": "Системний промпт:",
        "grp_audio": "Аудіо",
        "capture_system_audio": "Захоплювати системне аудіо (динаміки)",
        "grp_appearance": "Зовнішній вигляд",
        "theme": "Тема:",
        "always_on_top": "Завжди зверху",
        "opacity": "Прозорість:",
        "save_btn": "Зберегти",
        "cancel_btn": "Скасувати",
        "about": "Про програму",
    },
    "es": {
        "transcribe": "Transcribir",
        "summarize": "Resumir",
        "import_audio": "Importar audio",
        "copy_all": "Copiar todo",
        "save_md": "Guardar MD",
        "save_wav": "Guardar WAV",
        "play": "▶ Reproducir",
        "stop_play": "■ Detener",
        "new_session": "Nueva sesión",
        "recording": "Grabando…",
        "ready": "Listo",
        "transcribing": "Transcribiendo… (espere un momento)",
        "transcription_complete": "Transcripción completa",
        "generating_summary": "Generando resumen…",
        "summary_ready": "Resumen listo",
        "no_recording": "No hay grabación para transcribir",
        "copied": "Copiado al portapapeles",
        "transcription": "Transcripción",
        "summary_notes": "Resumen && Notas",
        "transcribe_first": "Primero transcriba antes de resumir",
        "recorded": "Grabado",
        "session": "sesión",
        "settings_title": "LiveScriber Configuración",
        "grp_transcription": "Transcripción",
        "whisper_model": "Modelo Whisper:",
        "language": "Idioma:",
        "auto_detect": "detección automática (dejar vacío)",
        "live_transcription_label": "Transcripción en vivo durante la grabación (experimental)",
        "auto_translate_label": "Traducir automáticamente al inglés (Append English)",
        "grp_summarization": "Resumen",
        "backend": "Backend:",
        "system_prompt": "Indicación del sistema:",
        "grp_audio": "Audio",
        "capture_system_audio": "Capturar audio del sistema (altavoces)",
        "grp_appearance": "Apariencia",
        "theme": "Tema:",
        "always_on_top": "Siempre visible",
        "opacity": "Opacidad:",
        "save_btn": "Guardar",
        "cancel_btn": "Cancelar",
        "about": "Acerca de",
    },
    "fr": {
        "transcribe": "Transcrire",
        "summarize": "Résumer",
        "import_audio": "Importer l'audio",
        "copy_all": "Tout copier",
        "save_md": "Enregistrer MD",
        "save_wav": "Enregistrer WAV",
        "play": "▶ Lire",
        "stop_play": "■ Arrêter",
        "new_session": "Nouvelle session",
        "recording": "Enregistrement…",
        "ready": "Prêt",
        "transcribing": "Transcription en cours… (veuillez patienter)",
        "transcription_complete": "Transcription terminée",
        "generating_summary": "Génération du résumé…",
        "summary_ready": "Résumé prêt",
        "no_recording": "Aucun enregistrement à transcrire",
        "copied": "Copié dans le presse-papiers",
        "transcription": "Transcription",
        "summary_notes": "Résumé && Notes",
        "transcribe_first": "Transcrivez d'abord avant de résumer",
        "recorded": "Enregistré",
        "session": "session",
        "settings_title": "LiveScriber Paramètres",
        "grp_transcription": "Transcription",
        "whisper_model": "Modèle Whisper :",
        "language": "Langue :",
        "auto_detect": "détection automatique (laisser vide)",
        "live_transcription_label": "Transcription en direct pendant l'enregistrement (expérimental)",
        "auto_translate_label": "Traduction automatique en anglais (Append English)",
        "grp_summarization": "Résumé",
        "backend": "Backend :",
        "system_prompt": "Invite système :",
        "grp_audio": "Audio",
        "capture_system_audio": "Capturer l'audio système (haut-parleurs)",
        "grp_appearance": "Apparence",
        "theme": "Thème :",
        "always_on_top": "Toujours au premier plan",
        "opacity": "Opacité :",
        "save_btn": "Enregistrer",
        "cancel_btn": "Annuler",
        "about": "À propos",
    },
    "de": {
        "transcribe": "Transkribieren",
        "summarize": "Zusammenfassen",
        "import_audio": "Audio importieren",
        "copy_all": "Alles kopieren",
        "save_md": "MD speichern",
        "save_wav": "WAV speichern",
        "play": "▶ Abspielen",
        "stop_play": "■ Stopp",
        "new_session": "Neue Sitzung",
        "recording": "Aufnahme…",
        "ready": "Bereit",
        "transcribing": "Transkription läuft… (bitte warten)",
        "transcription_complete": "Transkription abgeschlossen",
        "generating_summary": "Zusammenfassung wird erstellt…",
        "summary_ready": "Zusammenfassung fertig",
        "no_recording": "Keine Aufnahme zum Transkribieren",
        "copied": "In die Zwischenablage kopiert",
        "transcription": "Transkription",
        "summary_notes": "Zusammenfassung && Notizen",
        "transcribe_first": "Erst transkribieren, dann zusammenfassen",
        "recorded": "Aufgenommen",
        "session": "Sitzung",
        "settings_title": "LiveScriber Einstellungen",
        "grp_transcription": "Transkription",
        "whisper_model": "Whisper-Modell:",
        "language": "Sprache:",
        "auto_detect": "automatische Erkennung (leer lassen)",
        "live_transcription_label": "Live-Transkription während der Aufnahme (experimentell)",
        "auto_translate_label": "Automatische Übersetzung ins Englische (Append English)",
        "grp_summarization": "Zusammenfassung",
        "backend": "Backend:",
        "system_prompt": "Systemaufforderung:",
        "grp_audio": "Audio",
        "capture_system_audio": "Systemaudio aufnehmen (Lautsprecher)",
        "grp_appearance": "Erscheinungsbild",
        "theme": "Design:",
        "always_on_top": "Immer im Vordergrund",
        "opacity": "Transparenz:",
        "save_btn": "Speichern",
        "cancel_btn": "Abbrechen",
        "about": "Über",
    },
    "pt": {
        "transcribe": "Transcrever",
        "summarize": "Resumir",
        "import_audio": "Importar áudio",
        "copy_all": "Copiar tudo",
        "save_md": "Salvar MD",
        "save_wav": "Salvar WAV",
        "play": "▶ Reproduzir",
        "stop_play": "■ Parar",
        "new_session": "Nova sessão",
        "recording": "Gravando…",
        "ready": "Pronto",
        "transcribing": "Transcrevendo… (aguarde um momento)",
        "transcription_complete": "Transcrição concluída",
        "generating_summary": "Gerando resumo…",
        "summary_ready": "Resumo pronto",
        "no_recording": "Nenhuma gravação para transcrever",
        "copied": "Copiado para a área de transferência",
        "transcription": "Transcrição",
        "summary_notes": "Resumo && Notas",
        "transcribe_first": "Transcreva primeiro antes de resumir",
        "recorded": "Gravado",
        "session": "sessão",
        "settings_title": "LiveScriber Configurações",
        "grp_transcription": "Transcrição",
        "whisper_model": "Modelo Whisper:",
        "language": "Idioma:",
        "auto_detect": "detecção automática (deixar vazio)",
        "live_transcription_label": "Transcrição ao vivo durante a gravação (experimental)",
        "auto_translate_label": "Tradução automática para inglês (Append English)",
        "grp_summarization": "Resumo",
        "backend": "Backend:",
        "system_prompt": "Prompt do sistema:",
        "grp_audio": "Áudio",
        "capture_system_audio": "Capturar áudio do sistema (alto-falantes)",
        "grp_appearance": "Aparência",
        "theme": "Tema:",
        "always_on_top": "Sempre no topo",
        "opacity": "Opacidade:",
        "save_btn": "Salvar",
        "cancel_btn": "Cancelar",
        "about": "Sobre",
    },
    "ar": {
        "transcribe": "نسخ صوتي",
        "summarize": "تلخيص",
        "import_audio": "استيراد صوت",
        "copy_all": "نسخ الكل",
        "save_md": "حفظ MD",
        "save_wav": "حفظ WAV",
        "play": "▶ تشغيل",
        "stop_play": "■ إيقاف",
        "new_session": "جلسة جديدة",
        "recording": "جارٍ التسجيل…",
        "ready": "جاهز",
        "transcribing": "جارٍ النسخ… (يرجى الانتظار)",
        "transcription_complete": "اكتمل النسخ",
        "generating_summary": "جارٍ إنشاء الملخص…",
        "summary_ready": "الملخص جاهز",
        "no_recording": "لا يوجد تسجيل للنسخ",
        "copied": "تم النسخ إلى الحافظة",
        "transcription": "النسخ الصوتي",
        "summary_notes": "الملخص && الملاحظات",
        "transcribe_first": "انسخ أولاً قبل التلخيص",
        "recorded": "تم التسجيل",
        "session": "جلسة",
        "settings_title": "LiveScriber الإعدادات",
        "grp_transcription": "النسخ الصوتي",
        "whisper_model": "نموذج Whisper:",
        "language": "اللغة:",
        "auto_detect": "اكتشاف تلقائي (اتركه فارغاً)",
        "live_transcription_label": "نسخ مباشر أثناء التسجيل (تجريبي)",
        "auto_translate_label": "ترجمة تلقائية إلى الإنجليزية (Append English)",
        "grp_summarization": "التلخيص",
        "backend": "الواجهة الخلفية:",
        "system_prompt": "موجه النظام:",
        "grp_audio": "الصوت",
        "capture_system_audio": "التقاط صوت النظام (مكبرات الصوت)",
        "grp_appearance": "المظهر",
        "theme": "السمة:",
        "always_on_top": "دائماً في المقدمة",
        "opacity": "الشفافية:",
        "save_btn": "حفظ",
        "cancel_btn": "إلغاء",
        "about": "حول",
    },
}

_EN = _TRANSLATIONS["en"]


def t(key: str, lang: str = "en") -> str:
    """Return the translated string for *key* in *lang*, falling back to English."""
    return _TRANSLATIONS.get(lang, _EN).get(key, _EN.get(key, key))


# ── Translated system prompts for the summarizer ──────────────────────────
# Each prompt is a complete, native-language version of the default system
# prompt. This avoids asking the LLM to "respond in X" and instead gives
# it the full instruction in the target language from the start.

SYSTEM_PROMPTS: dict[str, str] = {
    "en": (
        "You are a note-taking assistant. Given a transcript of spoken audio, produce clear, "
        "organized notes. The audio may be a meeting, a solo brainstorm, troubleshooting session, "
        "or any spoken thoughts. Adapt your format to fit the content:\n"
        "- Start with a brief summary (2-3 sentences)\n"
        "- Key points or topics discussed as bullet points\n"
        "- Any decisions, conclusions, or solutions reached\n"
        "- Action items or next steps if mentioned\n"
        "Be concise and factual. Do NOT ask questions, add commentary, or include anything "
        "not present in the transcript. Output only the notes."
    ),
    "ko": (
        "당신은 노트 작성 도우미입니다. 음성 녹음의 텍스트 변환본을 받아 명확하고 "
        "정리된 노트를 작성하세요. 회의, 브레인스토밍, 문제 해결, "
        "또는 구두 메모일 수 있습니다. 내용에 맞게 형식을 조정하세요:\n"
        "- 간단한 요약으로 시작 (2-3문장)\n"
        "- 논의된 핵심 사항을 글머리 기호로 정리\n"
        "- 결정사항, 결론 또는 해결책\n"
        "- 언급된 실행 항목 또는 다음 단계\n"
        "간결하고 사실에 기반하세요. 질문하거나, 논평을 추가하거나, "
        "텍스트 변환본에 없는 내용을 포함하지 마세요. 노트만 출력하세요. "
        "반드시 한국어로 작성하세요."
    ),
    "ja": (
        "あなたはノート作成アシスタントです。音声録音の文字起こしを受け取り、明確で "
        "整理されたノートを作成してください。会議、ブレインストーミング、トラブルシューティング、"
        "または音声メモの場合があります。内容に合わせて形式を調整してください：\n"
        "- 簡潔な要約から始める（2〜3文）\n"
        "- 議論された重要なポイントを箇条書きで整理\n"
        "- 決定事項、結論、または解決策\n"
        "- 言及されたアクションアイテムまたは次のステップ\n"
        "簡潔かつ事実に基づいてください。質問したり、コメントを追加したり、"
        "文字起こしにない内容を含めないでください。ノートのみを出力してください。"
        "必ず日本語で記述してください。"
    ),
    "uk": (
        "Ви — помічник для створення нотаток. Отримавши транскрипцію аудіозапису, створіть чіткі, "
        "організовані нотатки. Це може бути нарада, мозковий штурм, усунення проблем "
        "або усні думки. Адаптуйте формат до змісту:\n"
        "- Починайте з короткого підсумку (2-3 речення)\n"
        "- Ключові моменти або обговорені теми як маркований список\n"
        "- Прийняті рішення, висновки або знайдені рішення\n"
        "- Згадані завдання або наступні кроки\n"
        "Будьте стислі та фактичні. НЕ ставте питань, не додавайте коментарів і не включайте "
        "нічого, чого немає в транскрипції. Виводьте лише нотатки. "
        "Обов'язково пишіть українською мовою."
    ),
    "es": (
        "Eres un asistente de toma de notas. Dada una transcripción de audio hablado, produce notas "
        "claras y organizadas. Puede ser una reunión, lluvia de ideas, sesión de resolución de problemas "
        "o pensamientos hablados. Adapta el formato al contenido:\n"
        "- Comienza con un breve resumen (2-3 oraciones)\n"
        "- Puntos clave o temas discutidos como viñetas\n"
        "- Decisiones, conclusiones o soluciones alcanzadas\n"
        "- Elementos de acción o próximos pasos mencionados\n"
        "Sé conciso y factual. NO hagas preguntas, añadas comentarios ni incluyas nada "
        "que no esté en la transcripción. Solo produce las notas. "
        "Escribe completamente en español."
    ),
    "fr": (
        "Vous êtes un assistant de prise de notes. À partir d'une transcription audio, produisez des notes "
        "claires et organisées. Il peut s'agir d'une réunion, d'un brainstorming, d'une session de dépannage "
        "ou de pensées parlées. Adaptez le format au contenu :\n"
        "- Commencez par un bref résumé (2-3 phrases)\n"
        "- Points clés ou sujets discutés sous forme de puces\n"
        "- Décisions, conclusions ou solutions trouvées\n"
        "- Actions à entreprendre ou prochaines étapes mentionnées\n"
        "Soyez concis et factuel. NE posez PAS de questions, n'ajoutez pas de commentaires et n'incluez rien "
        "qui ne figure pas dans la transcription. Produisez uniquement les notes. "
        "Rédigez entièrement en français."
    ),
    "de": (
        "Sie sind ein Notiz-Assistent. Erstellen Sie aus einer Audiotranskription klare, "
        "organisierte Notizen. Es kann sich um ein Meeting, Brainstorming, eine Fehlerbehebung "
        "oder gesprochene Gedanken handeln. Passen Sie das Format an den Inhalt an:\n"
        "- Beginnen Sie mit einer kurzen Zusammenfassung (2-3 Sätze)\n"
        "- Wichtige Punkte oder besprochene Themen als Aufzählung\n"
        "- Getroffene Entscheidungen, Schlussfolgerungen oder Lösungen\n"
        "- Erwähnte Aufgaben oder nächste Schritte\n"
        "Seien Sie prägnant und sachlich. Stellen Sie KEINE Fragen, fügen Sie keine Kommentare hinzu "
        "und nehmen Sie nichts auf, was nicht in der Transkription steht. Geben Sie nur die Notizen aus. "
        "Schreiben Sie vollständig auf Deutsch."
    ),
    "pt": (
        "Você é um assistente de anotações. A partir de uma transcrição de áudio falado, produza notas "
        "claras e organizadas. Pode ser uma reunião, brainstorming, sessão de resolução de problemas "
        "ou pensamentos falados. Adapte o formato ao conteúdo:\n"
        "- Comece com um breve resumo (2-3 frases)\n"
        "- Pontos-chave ou tópicos discutidos como marcadores\n"
        "- Decisões, conclusões ou soluções alcançadas\n"
        "- Itens de ação ou próximos passos mencionados\n"
        "Seja conciso e factual. NÃO faça perguntas, adicione comentários ou inclua nada "
        "que não esteja na transcrição. Produza apenas as notas. "
        "Escreva completamente em português."
    ),
    "ar": (
        "أنت مساعد لتدوين الملاحظات. بناءً على نص مكتوب من تسجيل صوتي، أنتج ملاحظات "
        "واضحة ومنظمة. قد يكون اجتماعاً أو عصفاً ذهنياً أو جلسة حل مشكلات "
        "أو أفكاراً منطوقة. كيّف الشكل حسب المحتوى:\n"
        "- ابدأ بملخص موجز (2-3 جمل)\n"
        "- النقاط الرئيسية أو المواضيع التي نوقشت كنقاط\n"
        "- القرارات أو الاستنتاجات أو الحلول المتوصل إليها\n"
        "- بنود العمل أو الخطوات التالية المذكورة\n"
        "كن موجزاً وواقعياً. لا تطرح أسئلة ولا تضف تعليقات ولا تتضمن أي شيء "
        "غير موجود في النص. أخرج الملاحظات فقط. "
        "اكتب بالكامل باللغة العربية."
    ),
}


def get_system_prompt(lang: str = "en") -> str:
    """Return the system prompt in the given language, falling back to English."""
    return SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["en"])


# ── Copilot CLI specific prompts ──────────────────────────────────────────
# Copilot CLI is a coding assistant and rejects generic note-taking prompts.
# These prompts frame the task as generating documentation from a transcript,
# which Copilot accepts as a code-adjacent task.

COPILOT_PROMPTS: dict[str, str] = {
    "en": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes.\n\n"
        "Structure:\n"
        "- A brief summary (2-3 sentences)\n"
        "- Key points discussed as bullet points\n"
        "- Any decisions or conclusions reached\n"
        "- Action items or next steps if mentioned\n\n"
        "Transcript:\n\n"
    ),
    "ko": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes. Write entirely in Korean (한국어).\n\n"
        "구조:\n"
        "- 간단한 요약 (2-3문장)\n"
        "- 논의된 핵심 사항을 글머리 기호로 정리\n"
        "- 결정사항 또는 결론\n"
        "- 실행 항목 또는 다음 단계\n\n"
        "텍스트 변환본:\n\n"
    ),
    "ja": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes. Write entirely in Japanese (日本語).\n\n"
        "構造：\n"
        "- 簡潔な要約（2〜3文）\n"
        "- 議論された重要なポイントを箇条書きで\n"
        "- 決定事項または結論\n"
        "- アクションアイテムまたは次のステップ\n\n"
        "文字起こし：\n\n"
    ),
    "uk": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes. Write entirely in Ukrainian (Українська).\n\n"
        "Структура:\n"
        "- Короткий підсумок (2-3 речення)\n"
        "- Ключові моменти як маркований список\n"
        "- Прийняті рішення або висновки\n"
        "- Завдання або наступні кроки\n\n"
        "Транскрипція:\n\n"
    ),
    "es": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes. Write entirely in Spanish (Español).\n\n"
        "Estructura:\n"
        "- Un breve resumen (2-3 oraciones)\n"
        "- Puntos clave discutidos como viñetas\n"
        "- Decisiones o conclusiones alcanzadas\n"
        "- Elementos de acción o próximos pasos\n\n"
        "Transcripción:\n\n"
    ),
    "fr": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes. Write entirely in French (Français).\n\n"
        "Structure :\n"
        "- Un bref résumé (2-3 phrases)\n"
        "- Points clés discutés sous forme de puces\n"
        "- Décisions ou conclusions prises\n"
        "- Actions à entreprendre ou prochaines étapes\n\n"
        "Transcription :\n\n"
    ),
    "de": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes. Write entirely in German (Deutsch).\n\n"
        "Struktur:\n"
        "- Eine kurze Zusammenfassung (2-3 Sätze)\n"
        "- Wichtige Punkte als Aufzählung\n"
        "- Getroffene Entscheidungen oder Schlussfolgerungen\n"
        "- Aufgaben oder nächste Schritte\n\n"
        "Transkription:\n\n"
    ),
    "pt": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes. Write entirely in Portuguese (Português).\n\n"
        "Estrutura:\n"
        "- Um breve resumo (2-3 frases)\n"
        "- Pontos-chave discutidos como marcadores\n"
        "- Decisões ou conclusões alcançadas\n"
        "- Itens de ação ou próximos passos\n\n"
        "Transcrição:\n\n"
    ),
    "ar": (
        "You are acting as a backend text processing service for the LiveScriber app. "
        "Your only job is to process the transcript below into structured notes. "
        "Do NOT ask questions, offer help with code, or add any commentary. "
        "Output ONLY the formatted notes. Write entirely in Arabic (العربية).\n\n"
        "الهيكل:\n"
        "- ملخص موجز (2-3 جمل)\n"
        "- النقاط الرئيسية كنقاط\n"
        "- القرارات أو الاستنتاجات\n"
        "- بنود العمل أو الخطوات التالية\n\n"
        "النص:\n\n"
    ),
}


def get_copilot_prompt(lang: str = "en", append_english: bool = False) -> str:
    """Return the Copilot-specific prompt in the given language.

    When append_english is True and lang is not English, adds an instruction
    to produce bilingual output (native language first, then English).
    """
    prompt = COPILOT_PROMPTS.get(lang, COPILOT_PROMPTS["en"])
    if append_english and lang != "en":
        lang_name = {
            "ko": "Korean", "ja": "Japanese", "uk": "Ukrainian",
            "es": "Spanish", "fr": "French", "de": "German",
            "pt": "Portuguese", "ar": "Arabic",
        }.get(lang, lang)
        prompt = prompt.replace(
            "Transcript:\n\n",
            f"IMPORTANT: First write the notes in {lang_name}, then add a section "
            f"titled '**English Summary:**' with the same notes translated to English. "
            f"Output both sections.\n\nTranscript:\n\n"
        )
        # Also handle non-English "Transcript:" labels
        for label in ["텍스트 변환본:", "文字起こし:", "Транскрипція:", "Transcripción:",
                       "Transcription :", "Transkription:", "Transcrição:", "النص:"]:
            prompt = prompt.replace(
                f"{label}\n\n",
                f"IMPORTANT: First write the notes in {lang_name}, then add a section "
                f"titled '**English Summary:**' with the same notes translated to English. "
                f"Output both sections.\n\n{label}\n\n"
            )
    return prompt
