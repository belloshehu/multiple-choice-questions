from django import template

register = template.Library()

@register.filter(name="uppercase")
def upper_case(value):
    return value.upper()


@register.filter(name="passage_questions")
def get_questions_under_passage(value, questions):
    ''' Returns list of questions under a given passage.'''
    questions_with_passage = []
    added_questions = []
    # check if question is not already fitered.
    if value not in added_questions:
        for question in questions:
            if (question.passage == value.passage) and (question not in added_questions):
                questions_with_passage.append(question)
    return questions_with_passage


@register.filter(name='answers')
def get_choices(question, choices):
    ''' Returns choices for a question'''
    return [ choice for choice in choices if choice.question==question]

@register.filter(name='is_none')
def is_none(value):
    return value == None

@register.filter(name='is_not_none')
def is_not_none(value):
    return value != None

@register.filter(name='description')
def get_description(value):
    return value.description