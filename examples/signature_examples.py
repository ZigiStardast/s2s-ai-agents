"""Mali, sekvencijalni primeri DSPy Signatures za početnike."""

# Primeri su pojednostavljeni za radionicu i prate ideje iz DSPy
# dokumentacije o Signatures.
# https://dspy.ai/3.1.2/learn/programming/signatures/

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

from src.config import configure_dspy, load_settings


def main() -> None:
    """Podesi DSPy i pokreni trenutno otključan primer."""

    settings = load_settings()
    if settings.mode == "mock" or not settings.api_key:
        print("DSPy primer zahteva live režim i API ključ u .env.")
        return

    import dspy

    configure_dspy(settings)

    # ============================================================
    # PRIMER 1 — PITANJE -> ODGOVOR
    # ============================================================
    qa = dspy.Predict("question -> answer")
    result = qa(question="Koliko mačor ima nogu?")

    # "question" je ulazno polje.
    # "answer" je izlazno polje.
    # DSPy koristi nazive polja da razume njihove uloge.
    print("----------------------------------------")
    print("PRIMER 1: QUESTION -> ANSWER")
    print("----------------------------------------")
    print("Input:", "Koliko nogu ima mačka?")
    print("Output:", result.answer)

    # ============================================================
    # PRIMER 2 — TIPIZIRANI IZLAZ
    # ============================================================
    # Otkomentarišite ovaj ceo odeljak tek nakon rada sa Primerom 1.
    #sentence = "Obožavam palačinke."
    #sentiment_predictor = dspy.Predict("sentence -> sentiment: bool")
    #sentiment_result = sentiment_predictor(sentence=sentence)
    #print("----------------------------------------")
    #print("PRIMER 2: TYPED OUTPUT")
    #print("----------------------------------------")
    #print("Sentence:", sentence)
    #print("Sentiment:", sentiment_result.sentiment)
    #print("Python type:", type(sentiment_result.sentiment).__name__)

    # ============================================================
    # PRIMER 3 — SAŽIMANJE
    # ============================================================
    # Imena polja opisuju šta šaljemo i šta očekujemo nazad.
    # text = "Marko je otišao u prodavnicu po mleko. Kupio je i čokoladu. Zaboravio je mleko."
    # summarize = dspy.Predict("text -> summary")
    # summary_result = summarize(text=text)
    # print("----------------------------------------")
    # print("PRIMER 3: SUMMARIZATION")
    # print("----------------------------------------")
    # print("Text:", text)
    # print("Summary:", summary_result.summary)

    # ============================================================
    # PRIMER 4 — VIŠE ULAZA
    # ============================================================
    # Jedan Signature može da primi više imenovanih ulaza.
    # context = "Maza je mačka. Maza ima 4 godine."
    # question = "Koliko godina ima Maza?"
    # context_qa = dspy.Predict("context: str, question: str -> answer: str")
    # context_result = context_qa(context=context, question=question)
    # print("----------------------------------------")
    # print("PRIMER 4: MULTIPLE INPUTS")
    # print("----------------------------------------")
    # print("Context:", context)
    # print("Question:", question)
    # print("Answer:", context_result.answer)

    # ============================================================
    # PRIMER 5 — VIŠE IZLAZA
    # ============================================================
    # Signature može da vrati više imenovanih izlaza.
    # animal = "mačka"
    # animal_predictor = dspy.Predict(
    #     "animal: str -> sound: str, number_of_legs: int"
    # )
    # animal_result = animal_predictor(animal=animal)
    # print("----------------------------------------")
    # print("PRIMER 5: MULTIPLE OUTPUTS")
    # print("----------------------------------------")
    # print("Animal:", animal)
    # print("Sound:", animal_result.sound)
    # print("Number of legs:", animal_result.number_of_legs)

    # ============================================================
    # PRIMER 6 — EKSPLICITNE INSTRUKCIJE
    # ============================================================
    # Nazivi polja opisuju šta ulazi i izlazi; instructions pojašnjavaju zadatak.
    # healthy_food = dspy.Signature(
    #     "food -> healthy: bool",
    #     instructions=(
    #         "Return True for ordinary nutritious foods such as fruit or vegetables. "
    #         "Return False for obvious candy or highly sugary sweets."
    #     ),
    # )
    # healthy_predictor = dspy.Predict(healthy_food)
    # healthy_result = healthy_predictor(food="jabuka")
    # print("----------------------------------------")
    # print("PRIMER 6: EXPLICIT INSTRUCTIONS")
    # print("----------------------------------------")
    # print("Food:", "jabuka")
    # print("Healthy:", healthy_result.healthy)

    # ============================================================
    # PRIMER 7 — SIGNATURE KAO KLASA
    # ============================================================
    # Klasa je korisna kada želimo jasniji opis zadatka i proširiv kod.
    # class DescribeAnimal(dspy.Signature):
    #     """Describe a common animal very briefly."""
    #
    #     animal: str = dspy.InputField()
    #     description: str = dspy.OutputField(
    #         desc="One short sentence describing the animal."
    #     )
    #
    # describe = dspy.Predict(DescribeAnimal)
    # describe_result = describe(animal="pingvin")
    # print("----------------------------------------")
    # print("PRIMER 7: CLASS-BASED SIGNATURE")
    # print("----------------------------------------")
    # print("Animal:", "pingvin")
    # print("Description:", describe_result.description)


if __name__ == "__main__":
    main()
