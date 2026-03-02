from external_apis import mk2, ugc, gaumont


def book_seat(theater, movie_name, date):
    """
    Dispatcher : appelle la bonne API selon le fournisseur de la salle.
    Chaque API a une signature différente — c'est le pattern Adapter.
    """
    if theater.provider == "mk2":
        return mk2.book_seat(
            theater_name=theater.name,
            movie_name=movie_name,
            date=date,
        )
    elif theater.provider == "ugc":
        return ugc.reserve(
            film=movie_name,
            salle=theater.name,
            horaire=date,
        )
    elif theater.provider == "gaumont":
        return gaumont.make_reservation({
            "movie": movie_name,
            "theater": theater.name,
            "when": date,
        })
    else:
        raise ValueError(f"Unknown provider: {theater.provider}")
