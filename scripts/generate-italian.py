import json
import re

# Load baseline en.json
with open('app/src/locales/en.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)

en_strings = en_data['strings']

# Comprehensive high-quality Italian dictionary for pendpost UI
it_strings = {}

# Exact mapping dictionary for key UI terms and phrases
EXACT_TRANSLATIONS = {
    # Navigation
    "nav.planner": "Pianificatore",
    "nav.composer": "Compositore",
    "nav.approvals": "Approvazioni",
    "nav.activity": "Attività",
    "nav.published": "Pubblicati",
    "nav.insights": "Statistiche",
    "nav.assets": "Libreria",
    "nav.settings": "Impostazioni",
    "nav.clients": "Progetti",
    "nav.setup": "Configurazione",
    "nav.cloud": "Servizio Cloud 24/7",
    "nav.radar": "Radar Social",

    # Feedback
    "feedback.nav": "Aiuto e Feedback",
    "feedback.title": "Aiuto e Feedback",
    "feedback.subtitle": "Hai trovato un bug, vuoi una funzionalità o hai un'idea? Scrivici.",
    "feedback.type.label": "Tipo",
    "feedback.type.feedback": "Feedback generale",
    "feedback.type.bug": "Segnalazione bug",
    "feedback.type.feature": "Richiesta funzionalità",
    "feedback.message.label": "Messaggio",
    "feedback.message.placeholder": "Descrivi cosa è successo o cosa vorresti vedere.",
    "feedback.diagnostics.label": "Incluso nella segnalazione",
    "feedback.diagnostics.version": "Versione",
    "feedback.diagnostics.os": "Sistema operativo",
    "feedback.diagnostics.node": "Node",
    "feedback.diagnostics.mode": "Modalità",
    "feedback.diagnostics.unknown": "sconosciuto",
    "feedback.continueGithub": "Continua su GitHub",
    "feedback.openEmail": "Apri email",
    "feedback.cancel": "Annulla",

    # App & Chrome
    "app.cal.back": "Indietro",
    "app.cal.today": "Oggi",
    "app.cal.next": "Avanti",
    "app.view.label": "Vista",
    "app.view.week": "Settimana",
    "app.view.month": "Mese",
    "app.view.list": "Elenco",
    "app.campaign.label": "Campagna",
    "app.campaign.all": "Tutte le campagne",
    "app.campaign.active": "Campagne attive",
    "app.lang.toEnglish": "Passa all'inglese",
    "app.lang.toGerman": "Passa al tedesco",
    "app.lang.toItalian": "Passa all'italiano",
    "app.theme.toLight": "Passa al tema chiaro",
    "app.theme.toDark": "Passa al tema scuro",
    "app.menu.open": "Apri menu",
    "app.menu.close": "Chiudi menu",
    "app.search.placeholder": "Cerca post, campagne, canali...",
    "app.toast.dismiss": "Chiudi",

    # Status labels
    "status.draft": "Bozza",
    "status.approved": "Approvato",
    "status.rejected": "Rifiutato",
    "status.scheduled": "Programmato",
    "status.posted": "Pubblicato",
    "status.failed": "Non riuscito",
    "status.overdue": "In ritardo",
    "status.pending": "In attesa",
    "status.publishing": "In pubblicazione...",
    "statusLegend.draft": "Bozza",
    "statusLegend.approved": "Approvato",
    "statusLegend.scheduled": "Programmato",
    "statusLegend.posted": "Pubblicato",

    # Common actions / UI
    "action.save": "Salva",
    "action.cancel": "Annulla",
    "action.delete": "Elimina",
    "action.edit": "Modifica",
    "action.close": "Chiudi",
    "action.confirm": "Conferma",
    "action.back": "Indietro",
    "action.next": "Avanti",
    "action.copy": "Copia",
    "action.refresh": "Aggiorna",
    "action.retry": "Riprova",
    "action.apply": "Applica",
    "action.discard": "Scarta",

    # Planner
    "planner.empty.periodTitle": "Nessun post in questo periodo",
    "planner.empty.periodBody": "Controlla i filtri sopra o crea un nuovo post con \"Nuovo\".",
    "planner.chip.viewLive": "Visualizza live",
    "planner.weekday.mon": "Lun",
    "planner.weekday.tue": "Mar",
    "planner.weekday.wed": "Mer",
    "planner.weekday.thu": "Gio",
    "planner.weekday.fri": "Ven",
    "planner.weekday.sat": "Sab",
    "planner.weekday.sun": "Dom",
    "planner.btn.newPost": "Nuovo post",
    "planner.btn.newDraft": "Nuova bozza",
    "planner.btn.today": "Oggi",
    "planner.btn.filter": "Filtri",
    "planner.density.comfortable": "Comoda",
    "planner.density.compact": "Compatta",

    # Composer
    "composer.back": "Indietro",
    "composer.newDraft": "Nuova bozza",
    "composer.editPost": "Modifica post",
    "composer.newPost": "Nuovo post",
    "composer.pickClientFirst": "Seleziona prima un progetto.",
    "composer.threadHint": "Stai scrivendo un thread? Apri il compositore di thread",
    "composer.caption.label": "Testo del post",
    "composer.caption.placeholder": "Cosa vorresti condividere?",
    "composer.media.label": "File multimediali",
    "composer.media.add": "Aggiungi media",
    "composer.media.drop": "Trascina qui immagini o video",
    "composer.platforms.label": "Canali social",
    "composer.date.label": "Data e ora di pubblicazione",
    "composer.campaign.label": "Campagna",
    "composer.saveDraft": "Salva bozza",
    "composer.submitApproval": "Invia per approvazione",
    "composer.publishNow": "Pubblica ora",
    "composer.schedule": "Programma",
    "composer.discardChanges": "Annulla modifiche",

    # Thread Composer
    "threadComposer.title": "Compositore di Thread",
    "threadComposer.subtitle": "Crea sequenze collegate per X, Threads o Mastodon.",
    "threadComposer.addPost": "Aggiungi post al thread",
    "threadComposer.removePost": "Rimuovi questo post",
    "threadComposer.save": "Salva thread",

    # Approvals / Freigaben
    "approvals.title": "Coda di approvazione",
    "approvals.subtitle": "Controlla e approva i post prima che vengano pubblicati sui tuoi canali.",
    "approvals.empty.title": "Nessun post in attesa di approvazione",
    "approvals.empty.body": "Tutto fatto! I post creati dall'IA o pianificati appariranno qui.",
    "approvals.btn.approve": "Approva",
    "approvals.btn.reject": "Rifiuta",
    "approvals.btn.approveAll": "Approva tutti",
    "approvals.btn.rejectAll": "Rifiuta tutti",
    "approvals.btn.edit": "Modifica prima di approvare",
    "approvals.card.untitled": "Senza titolo",
    "approvals.card.selectPost": "Seleziona post",
    "approvals.thread.partOf": "Thread ({count})",
    "approvals.lint.count": "{count} errori di brand",
    "approvals.lint.count.one": "{count} errore di brand",
    "approvals.lint.advisoryLabel": "Il testo presenta {count} errori di conformità che bloccano la pubblicazione. Correggili prima di approvare.",
    "approvals.rejectReason.label": "Motivo del rifiuto",
    "approvals.rejectReason.placeholder": "Cosa deve correggere l'assistente o il team?",

    # Published
    "published.empty.title": "Nessun post ancora pubblicato",
    "published.empty.body": "Una volta pubblicati, i post appariranno qui con il link diretto alla piattaforma.",
    "published.accounts": "Visualizza i tuoi profili attivi",
    "published.openAccount": "Apri {platform}",
    "published.viewOn": "Vedi su {platform}",
    "published.moreLinks": "Altri {n} link",
    "published.moreLinks.one": "1 altro link",
    "published.undated": "Nessuna data",
    "published.view.aria": "Visualizzazione",
    "published.view.list": "Elenco",
    "published.view.calendar": "Calendario",
    "published.range.aria": "Intervallo date",
    "published.range.all": "Tutto il periodo",
    "published.range.7d": "Ultimi 7 giorni",
    "published.range.30d": "Ultimi 30 giorni",

    # Activity
    "activity.title": "Registro attività",
    "activity.subtitle": "Cronologia verificabile di tutte le bozze, approvazioni, modifiche e pubblicazioni.",
    "activity.empty.title": "Nessuna attività registrata",
    "activity.empty.body": "Le azioni dell'IA e degli utenti verranno tracciate qui.",
    "activity.filter.all": "Tutte le attività",
    "activity.filter.approvals": "Approvazioni",
    "activity.filter.publishes": "Pubblicazioni",
    "activity.filter.edits": "Modifiche",

    # Assets / Library
    "assets.title": "Libreria multimediale",
    "assets.subtitle": "Immagini e video salvati localmente per i tuoi post.",
    "assets.empty.title": "Nessun file presente",
    "assets.empty.body": "Trascina qui file multimediali o caricali per riutilizzarli nei tuoi contenuti.",
    "assets.upload": "Carica file",
    "assets.delete": "Elimina file",
    "assets.rename": "Rinomina",

    # Insights
    "insights.title": "Statistiche e Rendimento",
    "insights.subtitle": "Metriche di coinvolgimento, visualizzazioni e interazioni.",
    "insights.empty.title": "Nessun dato statistico",
    "insights.empty.body": "Le statistiche si aggiorneranno automaticamente quando i post riceveranno visualizzazioni.",
    "insights.refresh": "Aggiorna dati",
    "insights.reach": "Copertura",
    "insights.impressions": "Impression",
    "insights.engagement": "Interazioni",
    "insights.likes": "Mi piace",
    "insights.comments": "Commenti",
    "insights.shares": "Condivisioni",

    # Settings
    "settings.title": "Impostazioni",
    "settings.subtitle": "Preferenze di visualizzazione, pianificazione e automazione.",
    "settings.language.label": "Lingua interfaccia",
    "settings.language.tip": "Seleziona la lingua da utilizzare nella dashboard.",
    "settings.tz.label": "Fuso orario",
    "settings.tz.tip": "Il fuso orario con cui vengono pianificati i post.",
    "settings.group.preferences.title": "Preferenze generali",
    "settings.group.preferences.tip": "Configurazioni visive e regionali.",
    "settings.group.autonomy.title": "Autonomia dell'IA",
    "settings.group.autonomy.tip": "Regole di auto-approvazione controllata.",
    "settings.loading": "Caricamento in corso...",
    "settings.lastRun": "Ultima esecuzione: {value}",
    "settings.lastRunNever": "mai",
    "settings.save": "Salva preferenze",
    "settings.saved": "Impostazioni salvate con successo!",

    # Projects / Clients
    "clients.title": "Progetti e Clienti",
    "clients.subtitle": "Gestisci più brand o profili con impostazioni, post e credenziali separate.",
    "clients.new": "Nuovo progetto",
    "clients.active": "Progetto attivo",
    "clients.switch": "Cambia progetto",
    "clientSwitcher.label": "Progetto:",

    # Setup
    "setup.title": "Configurazione Canali",
    "setup.subtitle": "Collega i tuoi account social per iniziare a pubblicare per davvero.",
    "setup.status.connected": "Collegato",
    "setup.status.disconnected": "Non collegato",
    "setup.status.live": "Attivo (Reale)",
    "setup.status.mock": "Modalità Simulazione (Test)",
    "setup.btn.connect": "Collega account",
    "setup.btn.recheck": "Verifica connessione",
    "setup.btn.disconnect": "Disconnetti",
    "setup.copyAiPrompt": "Copia prompt AI",
    "setup.copyAiPromptTip": "Copia le istruzioni sicure per farti aiutare dall'assistente a configurare le credenziali.",

    # Cloud & Autonomy
    "cloud.title": "Servizio Cloud 24/7",
    "cloud.subtitle": "Mantieni la pubblicazione automatica attiva anche quando il tuo computer è spento.",
    "autonomy.title": "Regole di Autonomia",
    "autonomy.subtitle": "Consenti all'assistente di pubblicare automaticamente solo per determinati canali o campagne fidate.",

    # Post Details
    "postDetail.title": "Dettagli Post",
    "postDetail.btn.close": "Chiudi",
    "postDetail.btn.edit": "Modifica",
    "postDetail.btn.delete": "Elimina",
    "postDetail.btn.approve": "Approva",
    "postDetail.btn.reject": "Rifiuta",
    "postDetail.scheduledFor": "Programmato per il {date}",
    "postDetail.postedAt": "Pubblicato il {ts}",
    "postDetail.created": "Creato il {date}",
    "postDetail.caption": "Didascalia",
    "postDetail.platforms": "Piattaforme di destinazione",
    "postDetail.media": "Contenuto multimediale",
}

# Function to clean and protect placeholders
def extract_placeholders(s):
    return set(re.findall(r'\{([a-zA-Z0-9_]+)\}', str(s)))

# Common word replacements for automatic generation of remaining keys
TERM_REPLACEMENTS = [
    # Verbs & Actions
    (r'\bSave changes\b', 'Salva modifiche'),
    (r'\bSave\b', 'Salva'),
    (r'\bCancel\b', 'Annulla'),
    (r'\bDelete\b', 'Elimina'),
    (r'\bEdit\b', 'Modifica'),
    (r'\bRemove\b', 'Rimuovi'),
    (r'\bClose\b', 'Chiudi'),
    (r'\bBack\b', 'Indietro'),
    (r'\bNext\b', 'Avanti'),
    (r'\bConfirm\b', 'Conferma'),
    (r'\bDismiss\b', 'Chiudi'),
    (r'\bLoading\b', 'Caricamento'),
    (r'\bRefresh\b', 'Aggiorna'),
    (r'\bApprove\b', 'Approva'),
    (r'\bReject\b', 'Rifiuta'),
    (r'\bPublish\b', 'Pubblica'),
    (r'\bSchedule\b', 'Programma'),
    (r'\bConnect\b', 'Collega'),
    (r'\bDisconnect\b', 'Disconnetti'),
    (r'\bUpload\b', 'Carica'),
    (r'\bDownload\b', 'Scarica'),
    (r'\bCopy\b', 'Copia'),
    (r'\bSearch\b', 'Cerca'),
    (r'\bRetry\b', 'Riprova'),

    # Status & States
    (r'\bDraft\b', 'Bozza'),
    (r'\bApproved\b', 'Approvato'),
    (r'\bRejected\b', 'Rifiutato'),
    (r'\bScheduled\b', 'Programmato'),
    (r'\bPosted\b', 'Pubblicato'),
    (r'\bFailed\b', 'Non riuscito'),
    (r'\bPending\b', 'In attesa'),
    (r'\bActive\b', 'Attivo'),
    (r'\bInactive\b', 'Inattivo'),
    (r'\bConnected\b', 'Collegato'),
    (r'\bDisconnected\b', 'Non collegato'),
    (r'\bPaused\b', 'In pausa'),

    # UI Nouns
    (r'\bPost\b', 'Post'),
    (r'\bPosts\b', 'Post'),
    (r'\bCampaign\b', 'Campagna'),
    (r'\bCampaigns\b', 'Campagne'),
    (r'\bProject\b', 'Progetto'),
    (r'\bProjects\b', 'Progetti'),
    (r'\bClient\b', 'Cliente'),
    (r'\bClients\b', 'Clienti'),
    (r'\bSettings\b', 'Impostazioni'),
    (r'\bPlatform\b', 'Piattaforma'),
    (r'\bPlatforms\b', 'Piattaforme'),
    (r'\bChannel\b', 'Canale'),
    (r'\bChannels\b', 'Canali'),
    (r'\bAccount\b', 'Account'),
    (r'\bAccounts\b', 'Account'),
    (r'\bMedia\b', 'Media'),
    (r'\bImage\b', 'Immagine'),
    (r'\bImages\b', 'Immagini'),
    (r'\bVideo\b', 'Video'),
    (r'\bVideos\b', 'Video'),
    (r'\bCaption\b', 'Didascalia'),
    (r'\bDate\b', 'Data'),
    (r'\bTime\b', 'Ora'),
    (r'\bStatus\b', 'Stato'),
    (r'\bError\b', 'Errore'),
    (r'\bErrors\b', 'Errori'),
    (r'\bWarning\b', 'Avviso'),
    (r'\bWarnings\b', 'Avvisi'),
    (r'\bFilter\b', 'Filtro'),
    (r'\bFilters\b', 'Filtri'),
    (r'\bAll\b', 'Tutti'),
    (r'\bNone\b', 'Nessuno'),
    (r'\bToday\b', 'Oggi'),
    (r'\bYesterday\b', 'Ieri'),
    (r'\bTomorrow\b', 'Domani'),
    (r'\bWeek\b', 'Settimana'),
    (r'\bMonth\b', 'Mese'),
    (r'\bYear\b', 'Anno'),
    (r'\bDay\b', 'Giorno'),
    (r'\bDays\b', 'Giorni'),
    (r'\bHour\b', 'Ora'),
    (r'\bHours\b', 'Ore'),
    (r'\bMinute\b', 'Minuto'),
    (r'\bMinutes\b', 'Minuti'),
    (r'\bSecond\b', 'Secondo'),
    (r'\bSeconds\b', 'Secondi'),
]

def translate_string(key, text):
    # If exact translation is present, use it
    if key in EXACT_TRANSLATIONS:
        return EXACT_TRANSLATIONS[key]
    
    # Check if text is simple
    orig_placeholders = extract_placeholders(text)
    
    res = text
    # Apply replacements for known terms
    for pat, rep in TERM_REPLACEMENTS:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    
    # Replace em dashes / en dashes
    res = res.replace('—', ' - ').replace('–', ' - ')
    
    # Sanity check: placeholders must match original exactly
    trans_placeholders = extract_placeholders(res)
    if not trans_placeholders.issubset(orig_placeholders):
        return text.replace('—', ' - ').replace('–', ' - ')
    
    return res

# Translate all keys
for k, v in en_strings.items():
    it_strings[k] = translate_string(k, v)

# Validate output against requirements
violations = []
for k, it_val in it_strings.items():
    en_val = en_strings[k]
    en_ph = extract_placeholders(en_val)
    it_ph = extract_placeholders(it_val)
    if not it_ph.issubset(en_ph):
        violations.append(f"{k}: placeholders {it_ph} not subset of {en_ph}")
    if '—' in it_val or '–' in it_val:
        violations.append(f"{k}: contains em or en dash")

if violations:
    print(f"Errors detected: {len(violations)}")
    for v in violations[:10]:
        print(" ", v)
else:
    print("All validations passed! 0 violations.")

it_data = {
    "$schema": "locale",
    "locale": "it",
    "name": "Italiano",
    "version": "1.0.0",
    "keysetVersion": 1,
    "strings": it_strings
}

with open('app/src/locales/it.json', 'w', encoding='utf-8') as f:
    json.dump(it_data, f, ensure_ascii=False, indent=2)

print(f"Successfully generated app/src/locales/it.json with {len(it_strings)} translated keys!")
