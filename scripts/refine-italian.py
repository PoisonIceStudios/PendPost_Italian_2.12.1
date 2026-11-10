import json
import re

with open('app/src/locales/en.json', 'r', encoding='utf-8') as f:
    en_strings = json.load(f)['strings']

with open('app/src/locales/it.json', 'r', encoding='utf-8') as f:
    it_data = json.load(f)
    it_strings = it_data['strings']

REFINEMENTS = {
    # FilterBar
    "filterBar.tab.all": "Tutti",
    "filterBar.tab.needs-you": "Richiede attenzione",
    "filterBar.tab.draft": "Bozze",
    "filterBar.tab.pending": "In attesa di approvazione",
    "filterBar.tab.scheduled": "Approvati",
    "filterBar.tab.posted": "Pubblicati",
    "filterBar.tab.rejected": "Rifiutati",
    "filterBar.tab.overdue": "In ritardo",
    "filterBar.tab.parked": "In pausa",
    "filterBar.more": "Altri",

    # App filter
    "app.filter.type": "Tipo",
    "app.filter.reset": "Reimposta",
    "app.filter.all": "Tutti",
    "app.filter.action": "Azione",
    "app.campaign.label": "Campagna",
    "app.campaign.all": "Tutte le campagne",
    "app.campaign.active": "Campagne attive",
    "app.campaign.markVisible": "Rendi visibile",
    "app.campaign.markInternal": "Segna come interna",
    "app.campaign.showInternal": "Mostra campagne interne",
    "app.view.label": "Vista",
    "app.view.week": "Settimana",
    "app.view.month": "Mese",
    "app.view.list": "Elenco",
    "app.cal.back": "Indietro",
    "app.cal.today": "Oggi",
    "app.cal.next": "Avanti",
    "app.theme.toLight": "Tema chiaro",
    "app.theme.toDark": "Tema scuro",
    "app.lang.toEnglish": "Passa all'inglese",
    "app.lang.toGerman": "Passa al tedesco",
    "app.lang.toItalian": "Passa all'italiano",
    "app.nav.openMenu": "Apri menu",

    # Range
    "format.rangeTo": "al",

    # Client Switcher & Sidebar
    "clientSwitcher.activeSublabel": "Progetto attivo",
    "clientSwitcher.allSub": "{n} progetti",
    "clientSwitcher.all": "Tutti i progetti",
    "clientSwitcher.heading": "Progetti",
    "clientSwitcher.create": "Nuovo progetto",
    "clientSwitcher.manage": "Gestisci progetti",
    "clientSwitcher.showArchived": "Mostra archiviati ({count})",
    "clientSwitcher.hideArchived": "Nascondi archiviati",
    "clientSwitcher.archived": "archiviato",
    "clientSwitcher.defaultHint": "iniziale",
    "clientSwitcher.health.blocked": "Azione bloccata (Meta-368)",
    "clientSwitcher.switched": "Passato a {name}",
    "clientSwitcher.switchFailed": "Impossibile passare a {name}",
    "clientSwitcher.noClient": "Nessun progetto",
    "clientSwitcher.switching": "Cambiamento in corso...",
    "clientSwitcher.active": "Attivo",
    "sidebar.tagline": "Pianificatore Social",
    "sidebar.newPost": "Nuovo post",
    "sidebar.newThread": "Nuovo thread",
    "sidebar.nextUp": "Prossimo post",
    "sidebar.noneScheduled": "Nessun post programmato",
    "sidebar.keepRunning": "Mantieni attivo per pubblicare all'orario stabilito",

    # Needs You Tray
    "tray.title": "Richiede attenzione",
    "tray.badge.tip": "Richiede attenzione: {count}. Apri l'elenco",
    "tray.cause.connect": "{lane} non collegato",
    "tray.cause.reconnect": "{lane} richiede un nuovo accesso",
    "tray.cause.edit": "{lane} ha rifiutato il contenuto",
    "tray.cause.resume": "Pubblicazione su {lane} in pausa",
    "tray.cause.cloud": "In attesa del servizio cloud",
    "tray.cause.manual": "{lane} richiede pubblicazione manuale",
    "tray.cause.discard": "Il thread su {lane} non esiste più",
    "tray.count.posts.one": "1 post",
    "tray.count.posts": "{count} post",
    "tray.count.replies.one": "1 risposta",
    "tray.count.replies": "{count} risposte",
    "tray.review": "Rivedi",
    "tray.reviewAria": "Rivedi {count} post",
    "tray.show": "Mostra",
    "tray.more": "Altri {count}",
    "tray.less": "Mostra meno",
    "tray.system.scheduler": "La pubblicazione da questo computer è in pausa. I post approvati sono in attesa.",
    "tray.system.start": "Riprendi pubblicazione",
    "tray.system.schedulerWaiting": "La pubblicazione da questo computer è in pausa. Completa prima la Configurazione.",
    "tray.system.manifest": "Impossibile leggere il piano editoriale. La pubblicazione è sospesa.",
    "tray.system.config": "Impossibile leggere il file delle impostazioni. La pubblicazione è sospesa.",
    "tray.system.actionBlock": "{label} ha un blocco azioni. Risolvilo in Meta Business Suite.",
    "tray.system.openSetup": "Apri Configurazione",
    "tray.system.post": "{title} non è stato pubblicato",
    "tray.system.open": "Apri post",
    "tray.agent.done.one": "L'assistente ha corretto 1 post, pronto per l'approvazione",
    "tray.agent.done": "L'assistente ha corretto {count} post, pronti per l'approvazione",
    "tray.cloud.affects": "Interessa {names}",

    # Status
    "status.draft": "Bozza",
    "status.approved": "Approvato",
    "status.scheduled": "Programmato",
    "status.posted": "Pubblicato",
    "status.rejected": "Rifiutato",
    "status.overdue": "In ritardo",
    "status.failed": "Non riuscito",
    "status.pending": "In attesa",
    "status.publishing": "In pubblicazione...",
    "status.parked": "In pausa",

    # Status Legend
    "statusLegend.title": "Legenda stati",
    "statusLegend.draft": "Bozza",
    "statusLegend.approved": "Approvato",
    "statusLegend.scheduled": "Programmato",
    "statusLegend.posted": "Pubblicato",
    "statusLegend.rejected": "Rifiutato",
    "statusLegend.overdue": "In ritardo",
    "statusLegend.parked": "In pausa",

    # Post types
    "type.post": "Post",
    "type.carousel": "Carosello",
    "type.reel": "Reel",
    "type.story": "Storia",
    "type.video": "Video",
    "type.article": "Articolo",
    "type.thread": "Thread",
    "type.poll": "Sondaggio",
    "typeShort.post": "Post",
    "typeShort.carousel": "Carosello",
    "typeShort.reel": "Reel",
    "typeShort.story": "Storia",
    "typeShort.video": "Video",
    "typeShort.article": "Articolo",
    "typeShort.thread": "Thread",

    # Published
    "published.verify.idle": "Verifica",
    "published.verify.loading": "Verifica in corso...",
    "published.verify.success": "Verificato",
    "published.verify.recheck": "Ricontrolla",
    "published.verify.notLive": "Non ancora online",
    "published.evergreen.filter": "Riciclabile ({n})",
    "published.recycle.action": "Ricicla",
    "published.empty.title": "Nessun post ancora pubblicato",
    "published.empty.body": "Quando i post andranno online appariranno qui con i link diretti.",
    "published.viewOn": "Vedi su {platform}",
    "published.openAccount": "Apri profilo {platform}",
    "published.moreLinks": "Altri {n} link",
    "published.moreLinks.one": "1 altro link",
    "published.undated": "Nessuna data",
    "published.range.all": "Tutto il periodo",
    "published.range.7d": "Ultimi 7 giorni",
    "published.range.30d": "Ultimi 30 giorni",

    # Activity check now
    "activity.checkNow.loading": "Pubblicazione in corso...",
    "activity.checkNow.success": "Pubblicato",
    "activity.checkNow.confirm.title": "Pubblicare i post scaduti per {client}?",
    "activity.checkNow.confirm.body": "Questo pubblicherà i post approvati scaduti per {client}. L'operazione non può essere annullata.",
    "activity.checkNow.btn": "Pubblica scaduti",

    # Planner
    "planner.empty.periodTitle": "Nessun post in questo periodo",
    "planner.empty.periodBody": "Controlla i filtri sopra o crea un post con \"Nuovo post\".",
    "planner.chip.viewLive": "Visualizza live",
    "planner.weekday.mon": "Lun",
    "planner.weekday.tue": "Mar",
    "planner.weekday.wed": "Mer",
    "planner.weekday.thu": "Gio",
    "planner.weekday.fri": "Ven",
    "planner.weekday.sat": "Sab",
    "planner.weekday.sun": "Dom",
    "planner.density.comfortable": "Comoda",
    "planner.density.compact": "Compatta",

    # Approvals
    "approvals.view.all": "Tutti i post",
    "approvals.view.toReview": "Da revisionare",
    "approvals.empty.title": "Nessun post in attesa di approvazione",
    "approvals.empty.body": "Tutto in ordine! I post da approvare appariranno qui.",
    "approvals.card.untitled": "Senza titolo",
    "approvals.card.selectPost": "Seleziona post",
    "approvals.thread.partOf": "Thread ({count})",
    "approvals.btn.approve": "Approva",
    "approvals.btn.reject": "Rifiuta",
    "approvals.btn.edit": "Modifica prima di approvare",
    "approvals.btn.approveAll": "Approva tutti",
    "approvals.btn.rejectAll": "Rifiuta tutti",

    # Composer
    "composer.newDraft": "Nuova bozza",
    "composer.newPost": "Nuovo post",
    "composer.editPost": "Modifica post",
    "composer.back": "Indietro",
    "composer.saveDraft": "Salva bozza",
    "composer.publishNow": "Pubblica ora",
    "composer.schedule": "Programma",
    "composer.caption.label": "Testo del post",
    "composer.caption.placeholder": "Cosa vorresti condividere?",
    "composer.media.label": "File multimediali",
    "composer.platforms.label": "Piattaforme di destinazione",
    "composer.date.label": "Data e ora di pubblicazione",
    "composer.campaign.label": "Campagna",

    # Post detail
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
    "postDetail.platforms": "Piattaforme",
    "postDetail.media": "Media",

    # Settings
    "settings.title": "Impostazioni",
    "settings.subtitle": "Preferenze di visualizzazione, pianificazione e automazione.",
    "settings.language.label": "Lingua interfaccia",
    "settings.language.tip": "Seleziona la lingua da utilizzare nella dashboard.",
    "settings.tz.label": "Fuso orario",
    "settings.tz.tip": "Il fuso orario con cui vengono pianificati i post.",
    "settings.save": "Salva preferenze",
    "settings.saved": "Impostazioni salvate con successo!",
}

def extract_placeholders(s):
    return set(re.findall(r'\{([a-zA-Z0-9_]+)\}', str(s)))

applied = 0
for k, v in REFINEMENTS.items():
    if k in en_strings:
        orig_ph = extract_placeholders(en_strings[k])
        new_ph = extract_placeholders(v)
        if new_ph.issubset(orig_ph) and '—' not in v and '–' not in v:
            it_strings[k] = v
            applied += 1
        else:
            print(f"Skipping {k}: placeholder mismatch or em/en dash")

print(f"Applied {applied} refined Italian translations!")

it_data['strings'] = it_strings

with open('app/src/locales/it.json', 'w', encoding='utf-8') as f:
    json.dump(it_data, f, ensure_ascii=False, indent=2)

print("Saved app/src/locales/it.json!")
