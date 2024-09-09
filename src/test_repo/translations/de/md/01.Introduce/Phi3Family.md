# Microsofts Phi-3 Familie

Die Phi-3-Modelle sind die leistungsfähigsten und kosteneffektivsten Small Language Models (SLMs), die derzeit verfügbar sind. Sie übertreffen Modelle gleicher und größerer Größe in einer Vielzahl von Sprach-, Logik-, Codierungs- und Mathematik-Benchmarks. Diese Veröffentlichung erweitert die Auswahl hochwertiger Modelle für Kunden und bietet praktischere Optionen für das Erstellen generativer KI-Anwendungen.

Die Phi-3-Familie umfasst Mini-, Klein-, Mittel- und Vision-Versionen, die auf Basis unterschiedlicher Parameteranzahlen trainiert wurden, um verschiedenen Anwendungsszenarien gerecht zu werden. Jedes Modell ist anweisungsoptimiert und wurde gemäß Microsofts Richtlinien für verantwortungsvolle KI, Sicherheits- und Sicherheitsstandards entwickelt, um eine sofortige Einsatzbereitschaft zu gewährleisten. Phi-3-mini übertrifft Modelle, die doppelt so groß sind, und Phi-3-klein und Phi-3-mittel übertreffen deutlich größere Modelle, einschließlich GPT-3.5T.

## Beispielaufgaben von Phi-3

| | |
|-|-|
|Aufgaben|Phi-3|
|Sprachaufgaben|Ja|
|Mathematik & Logik|Ja|
|Codierung|Ja|
|Funktionsaufruf|Nein|
|Selbstorchestrierung (Assistent)|Nein|
|Dedizierte Einbettungsmodelle|Nein|

## Phi-3-mini

Phi-3-mini, ein Sprachmodell mit 3,8 Milliarden Parametern, ist verfügbar auf [Microsoft Azure AI Studio](https://ai.azure.com/explore/models?selectedCollection=phi), [Hugging Face](https://huggingface.co/collections/microsoft/phi-3-6626e15e9585a200d2d761e3) und [Ollama](https://ollama.com/library/phi3). Es bietet zwei Kontextlängen: [128K](https://ai.azure.com/explore/models/Phi-3-mini-128k-instruct/version/9/registry/azureml) und [4K](https://ai.azure.com/explore/models/Phi-3-mini-4k-instruct/version/9/registry/azureml).

Phi-3-mini ist ein auf Transformern basierendes Sprachmodell mit 3,8 Milliarden Parametern. Es wurde mit hochwertigen Daten trainiert, die bildungsrelevante Informationen enthalten, ergänzt durch neue Datenquellen, die aus verschiedenen NLP-synthetischen Texten und sowohl internen als auch externen Chat-Datensätzen bestehen, was die Chat-Fähigkeiten erheblich verbessert. Darüber hinaus wurde Phi-3-mini nach dem Vortraining durch überwachte Feinabstimmung (SFT) und Direct Preference Optimization (DPO) speziell für Chat-Anwendungen optimiert. Nach diesem Nachtraining hat Phi-3-mini bedeutende Verbesserungen in mehreren Fähigkeiten gezeigt, insbesondere in den Bereichen Ausrichtung, Robustheit und Sicherheit. Das Modell ist Teil der Phi-3-Familie und kommt in der Mini-Version mit zwei Varianten, 4K und 128K, die die unterstützte Kontextlänge (in Token) darstellen.

![phi3modelminibenchmark](../../imgs/01/phi3minibenchmark.png)

![phi3modelminibenchmark128k](../../imgs/01/phi3minibenchmark128.png)

## Phi-3.5-mini-instruct 

[Phi-3.5 mini](https://ai.azure.com/explore/models/Phi-3.5-mini-instruct/version/1/registry/azureml) ist ein leichtgewichtiges, hochmodernes offenes Modell, das auf den für Phi-3 verwendeten Datensätzen basiert - synthetische Daten und gefilterte öffentlich zugängliche Websites - mit einem Fokus auf sehr hochwertige, logikdichte Daten. Das Modell gehört zur Phi-3-Modellfamilie und unterstützt eine Kontextlänge von 128K Token. Das Modell durchlief einen rigorosen Verbesserungsprozess, der sowohl überwachte Feinabstimmung, proximale Policy-Optimierung als auch direkte Präferenzoptimierung umfasste, um eine präzise Befolgung der Anweisungen und robuste Sicherheitsmaßnahmen sicherzustellen.

Phi-3.5 Mini hat 3,8 Milliarden Parameter und ist ein dichtes, nur dekodierendes Transformer-Modell, das denselben Tokenizer wie Phi-3 Mini verwendet.

![phi3miniinstruct](../../imgs/01/phi3miniinstructbenchmark.png)

Insgesamt erreicht das Modell mit nur 3,8 Milliarden Parametern ein ähnliches Niveau an mehrsprachigem Sprachverständnis und Logikfähigkeit wie wesentlich größere Modelle. Es ist jedoch aufgrund seiner Größe für bestimmte Aufgaben immer noch grundlegend begrenzt. Das Modell hat einfach nicht die Kapazität, zu viele Fakten zu speichern, weshalb Benutzer möglicherweise faktische Ungenauigkeiten erleben. Wir glauben jedoch, dass solche Schwächen durch die Ergänzung von Phi-3.5 mit einer Suchmaschine behoben werden können, insbesondere bei der Verwendung des Modells in RAG-Einstellungen.

### Sprachunterstützung

Die folgende Tabelle zeigt die mehrsprachige Fähigkeit des Phi-3 auf den mehrsprachigen MMLU-, MEGA- und mehrsprachigen MMLU-pro-Datensätzen. Insgesamt haben wir beobachtet, dass das Modell selbst mit nur 3,8 Milliarden aktiven Parametern bei mehrsprachigen Aufgaben sehr konkurrenzfähig ist im Vergleich zu anderen Modellen mit deutlich mehr aktiven Parametern.

![phi3minilanguagesupport](../../imgs/01/phi3miniinstructlanguagesupport.png)

## Phi-3-small

Phi-3-small, ein Sprachmodell mit 7 Milliarden Parametern, verfügbar in zwei Kontextlängen [128K](https://ai.azure.com/explore/models/Phi-3-small-128k-instruct/version/2/registry/azureml) und [8K.](https://ai.azure.com/explore/models/Phi-3-small-8k-instruct/version/2/registry/azureml) übertrifft GPT-3.5T in einer Vielzahl von Sprach-, Logik-, Codierungs- und Mathematik-Benchmarks.

Phi-3-small ist ein auf Transformern basierendes Sprachmodell mit 7 Milliarden Parametern. Es wurde mit hochwertigen Daten trainiert, die bildungsrelevante Informationen enthalten, ergänzt durch neue Datenquellen, die aus verschiedenen NLP-synthetischen Texten und sowohl internen als auch externen Chat-Datensätzen bestehen, was die Chat-Fähigkeiten erheblich verbessert. Darüber hinaus wurde Phi-3-small nach dem Vortraining durch überwachte Feinabstimmung (SFT) und Direct Preference Optimization (DPO) speziell für Chat-Anwendungen optimiert. Nach diesem Nachtraining hat Phi-3-small bedeutende Verbesserungen in mehreren Fähigkeiten gezeigt, insbesondere in den Bereichen Ausrichtung, Robustheit und Sicherheit. Phi-3-small wurde auch intensiver auf mehrsprachigen Datensätzen trainiert im Vergleich zu Phi-3-Mini. Die Modellfamilie bietet zwei Varianten, 8K und 128K, die die unterstützte Kontextlänge (in Token) darstellen.

![phi3modelsmall](../../imgs/01/phi3smallbenchmark.png)

![phi3modelsmall128k](../../imgs/01/phi3smallbenchmark128.png)

## Phi-3-medium

Phi-3-medium, ein Sprachmodell mit 14 Milliarden Parametern, verfügbar in zwei Kontextlängen [128K](https://ai.azure.com/explore/models/Phi-3-medium-128k-instruct/version/2/registry/azureml) und [4K.](https://ai.azure.com/explore/models/Phi-3-medium-4k-instruct/version/2/registry/azureml), setzt den Trend fort, indem es Gemini 1.0 Pro übertrifft.

Phi-3-medium ist ein auf Transformern basierendes Sprachmodell mit 14 Milliarden Parametern. Es wurde mit hochwertigen Daten trainiert, die bildungsrelevante Informationen enthalten, ergänzt durch neue Datenquellen, die aus verschiedenen NLP-synthetischen Texten und sowohl internen als auch externen Chat-Datensätzen bestehen, was die Chat-Fähigkeiten erheblich verbessert. Darüber hinaus wurde Phi-3-medium nach dem Vortraining durch überwachte Feinabstimmung (SFT) und Direct Preference Optimization (DPO) speziell für Chat-Anwendungen optimiert. Nach diesem Nachtraining hat Phi-3-medium bedeutende Verbesserungen in mehreren Fähigkeiten gezeigt, insbesondere in den Bereichen Ausrichtung, Robustheit und Sicherheit. Die Modellfamilie bietet zwei Varianten, 4K und 128K, die die unterstützte Kontextlänge (in Token) darstellen.

![phi3modelmedium](../../imgs/01/phi3mediumbenchmark.png)

![phi3modelmedium128k](../../imgs/01/phi3mediumbenchmark128.png)

> [!NOTE]
> Wir empfehlen den Wechsel zu Phi-3.5-MoE als Upgrade von Phi-3-medium, da das MoE-Modell ein viel besseres und kosteneffizienteres Modell ist.

## Phi-3-vision

Das [Phi-3-vision](https://ai.azure.com/explore/models/Phi-3-vision-128k-instruct/version/2/registry/azureml), ein multimodales Modell mit 4,2 Milliarden Parametern und Sprach- und Bildfähigkeiten, übertrifft größere Modelle wie Claude-3 Haiku und Gemini 1.0 Pro V in allgemeinen visuellen Logik-, OCR- und Tabellen- und Diagrammverständnisaufgaben.

Phi-3-vision ist das erste multimodale Modell in der Phi-3-Familie, das Text und Bilder zusammenführt. Phi-3-vision kann verwendet werden, um über reale Bilder nachzudenken und Text aus Bildern zu extrahieren und zu analysieren. Es wurde auch für das Verständnis von Diagrammen und Schaubildern optimiert und kann verwendet werden, um Einblicke zu generieren und Fragen zu beantworten. Phi-3-vision baut auf den Sprachfähigkeiten des Phi-3-mini auf und bietet weiterhin eine starke Sprach- und Bildlogikqualität in kleiner Größe.

![phi3modelvision](../../imgs/01/phi3visionbenchmark.png)

## Phi-3.5-vision

[Phi-3.5 Vision](https://ai.azure.com/explore/models/Phi-3.5-vision-instruct/version/1/registry/azureml) ist ein leichtgewichtiges, hochmodernes offenes multimodales Modell, das auf Datensätzen basiert, die - synthetische Daten und gefilterte öffentlich zugängliche Websites - mit einem Fokus auf sehr hochwertige, logikdichte Daten sowohl für Text als auch für Bilder umfassen. Das Modell gehört zur Phi-3-Modellfamilie, und die multimodale Version unterstützt eine Kontextlänge von 128K Token. Das Modell durchlief einen rigorosen Verbesserungsprozess, der sowohl überwachte Feinabstimmung als auch direkte Präferenzoptimierung umfasste, um eine präzise Befolgung der Anweisungen und robuste Sicherheitsmaßnahmen sicherzustellen.

Phi-3.5 Vision hat 4,2 Milliarden Parameter und enthält Bild-Encoder, Connector, Projektor und Phi-3 Mini Sprachmodell.

Das Modell ist für den breiten kommerziellen und Forschungsgebrauch in Englisch vorgesehen. Das Modell bietet Anwendungen für allgemeine KI-Systeme und Anwendungen mit visuellen und Texteingabefähigkeiten, die Folgendes erfordern:
1) Speicher-/Rechenbeschränkte Umgebungen.
2) Latenzgebundene Szenarien.
3) Allgemeines Bildverständnis.
4) OCR.
5) Verständnis von Diagrammen und Tabellen.
6) Vergleich mehrerer Bilder.
7) Zusammenfassung mehrerer Bilder oder Videoclips.

Das Phi-3.5-vision Modell ist darauf ausgelegt, die Forschung an effizienten Sprach- und multimodalen Modellen zu beschleunigen, um als Baustein für generative KI-basierte Funktionen zu dienen.

![phi35_vision](../../imgs/01/phi35visionbenchmark.png)

## Phi-3.5-MoE

[Phi-3.5 MoE](https://ai.azure.com/explore/models/Phi-3.5-MoE-instruct/version/1/registry/azureml) ist ein leichtgewichtiges, hochmodernes offenes Modell, das auf den für Phi-3 verwendeten Datensätzen basiert - synthetische Daten und gefilterte öffentlich zugängliche Dokumente - mit einem Fokus auf sehr hochwertige, logikdichte Daten. Das Modell unterstützt Mehrsprachigkeit und kommt mit einer Kontextlänge von 128K Token. Das Modell durchlief einen rigorosen Verbesserungsprozess, der sowohl überwachte Feinabstimmung, proximale Policy-Optimierung als auch direkte Präferenzoptimierung umfasste, um eine präzise Befolgung der Anweisungen und robuste Sicherheitsmaßnahmen sicherzustellen.

Phi-3 MoE hat 16x3,8 Milliarden Parameter mit 6,6 Milliarden aktiven Parametern, wenn 2 Experten verwendet werden. Das Modell ist ein mixture-of-expert dekodierendes Transformer-Modell, das den Tokenizer mit einer Vokabulargröße von 32.064 verwendet.

Das Modell ist für den breiten kommerziellen und Forschungsgebrauch in Englisch vorgesehen. Das Modell bietet Anwendungen für allgemeine KI-Systeme und Anwendungen, die Folgendes erfordern:

1) Speicher-/Rechenbeschränkte Umgebungen.
2) Latenzgebundene Szenarien.
3) Starke Logik (insbesondere Mathematik und Logik).

Das MoE-Modell ist darauf ausgelegt, die Forschung an Sprach- und multimodalen Modellen zu beschleunigen, um als Baustein für generative KI-basierte Funktionen zu dienen und erfordert zusätzliche Rechenressourcen.

![phi35moe_model](../../imgs/01/phi35moebenchmark.png)

> [!NOTE]
>
> Phi-3-Modelle schneiden bei faktischen Wissensbenchmarks (wie TriviaQA) nicht so gut ab, da die kleinere Modellgröße weniger Kapazität hat, um Fakten zu speichern.

## Phi Silica

Wir stellen Phi Silica vor, das aus der Phi-Serie von Modellen entwickelt wurde und speziell für die NPUs in Copilot+ PCs konzipiert ist. Windows ist die erste Plattform, die ein hochmodernes Small Language Model (SLM) speziell für die NPU und als vorinstallierte Software anbietet. Die Phi Silica API zusammen mit OCR, Studio Effects, Live Captions und Recall User Activity APIs wird im Juni in der Windows Copilot Library verfügbar sein. Weitere APIs wie Vector Embedding, RAG API und Text Summarization werden später folgen.

## **Finden Sie alle Phi-3-Modelle**

- [Azure AI](https://ai.azure.com/explore/models?selectedCollection=phi)
- [Hugging Face](https://huggingface.co/collections/microsoft/phi-3-6626e15e9585a200d2d761e3)

## ONNX-Modelle

Der Hauptunterschied zwischen den beiden ONNX-Modellen, „cpu-int4-rtn-block-32“ und „cpu-int4-rtn-block-32-acc-level-4“, liegt im Genauigkeitsgrad. Das Modell mit „acc-level-4“ ist darauf ausgelegt, Latenz und Genauigkeit zu balancieren, wobei eine geringe Genauigkeitseinbuße für eine bessere Leistung in Kauf genommen wird, was besonders für mobile Geräte geeignet sein könnte.

## Beispiel für die Modellauswahl

| | | | |
|-|-|-|-|
|Kundenbedarf|Aufgabe|Start mit|Weitere Details|
|Benötigt ein Modell, das einfach einen Nachrichtenverlauf zusammenfasst|Konversationszusammenfassung|Phi-3 Textmodell|Entscheidender Faktor hier ist, dass der Kunde eine klar definierte und einfache Sprachaufgabe hat|
|Eine kostenlose Mathe-Nachhilfe-App für Kinder|Mathematik und Logik|Phi-3 Textmodelle|Da die App kostenlos ist, möchten Kunden eine Lösung, die keine laufenden Kosten verursacht|
|Selbstüberwachende Autokamera|Bildanalyse|Phi-Vision|Benötigt eine Lösung, die ohne Internet am Rand funktioniert|
|Möchte einen KI-basierten Reisebuchungsagenten erstellen|Benötigt komplexe Planung, Funktionsaufrufe und Orchestrierung|GPT-Modelle|Benötigt die Fähigkeit zu planen, APIs aufzurufen, um Informationen zu sammeln und auszuführen|
|Möchte einen Copiloten für seine Mitarbeiter erstellen|RAG, mehrere Domänen, komplex und offen|GPT-Modelle|Offenes Szenario, benötigt breiteres Weltwissen, daher ist ein größeres Modell besser geeignet|

Haftungsausschluss: Die Übersetzung wurde von einem KI-Modell aus dem Original übersetzt und ist möglicherweise nicht perfekt. Bitte überprüfen Sie die Ausgabe und nehmen Sie gegebenenfalls notwendige Korrekturen vor.