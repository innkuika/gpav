from gpav_app.models import Person


def create_person_if_absent(person_id, name) -> Person:
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        person = Person(id=person_id, name=name)
        person.save()

    return person
