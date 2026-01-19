import pytest
from smartmailer.core.template import TemplateEngine, TemplateModel



class ExampleSchema(TemplateModel):
    name: str
    committee: str
    allotment: str
    email: str


# 1. Test basic variable substitution using {{ }}
def test_basic_variable_substitution():
    subject = "Hello {{ name }}"
    body = "Committee: {{ committee }}"

    template = TemplateEngine(subject=subject, body_text=body)

    data = ExampleSchema(
        name="Test User",
        committee="UNDP",
        allotment="India",
        email="test@example.com"
    )

    result = template.render(data)

    assert result["subject"] == "Hello Test User"
    assert result["text"] == "Committee: UNDP"


# 2. Test Jinja2 conditional rendering (if / else)
def test_conditional_rendering():
    body = """
    {% if committee == "UNDP" %}
    Special committee
    {% else %}
    Regular committee
    {% endif %}
    """

    template = TemplateEngine(body_text=body)

    data = ExampleSchema(
        name="Test User",
        committee="UNDP",
        allotment="India",
        email="test@example.com"
    )

    result = template.render(data)

    assert "Special committee" in result["text"]


# 3. Test missing variable handling (should raise error)
def test_missing_variable_raises_error():
    body = "Hello {{ fullname }}"

    template = TemplateEngine(body_text=body)

    data = ExampleSchema(
        name="Test User",
        committee="UNDP",
        allotment="India",
        email="test@example.com"
    )

    with pytest.raises(ValueError) as exc:
        template.render(data)

    assert "fullname" in str(exc.value)


# 4. Test invalid Jinja2 template syntax
def test_invalid_template_syntax():
    body = """
    {% if committee == "UNDP" %}
    Special committee
    """

    template = TemplateEngine(body_text=body)

    data = ExampleSchema(
        name="Test User",
        committee="UNDP",
        allotment="India",
        email="test@example.com"
    )

    with pytest.raises(ValueError):
        template.render(data)


# 5. Test schema validation for invalid field names
def test_invalid_schema_field_name():
    with pytest.raises(ValueError):

        class BadSchema(TemplateModel):
            fullName: str  # invalid (underscore ok, but uppercase not allowed)

        BadSchema(fullName="Test")

# 6. Test subject and body rendering independently
def test_subject_and_body_rendering():
    subject = "Mail for {{ name }}"
    body = "Hello {{ name }}"

    template = TemplateEngine(subject=subject, body_text=body)

    data = ExampleSchema(
        name="Test User",
        committee="UNDP",
        allotment="India",
        email="test@example.com"
    )

    result = template.render(data)

    assert result["subject"] == "Mail for Test User"
    assert result["text"] == "Hello Test User"


# 7. Test rendering for multiple recipients with different data
def test_multiple_recipients_rendering():
    body = """
    {% if committee == "UNDP" %}
    Special
    {% else %}
    Regular
    {% endif %}
    """

    template = TemplateEngine(body_text=body)

    data_1 = ExampleSchema(
        name="User A",
        committee="UNDP",
        allotment="India",
        email="a@example.com"
    )

    data_2 = ExampleSchema(
        name="User B",
        committee="ECOSOC",
        allotment="France",
        email="b@example.com"
    )

    result_1 = template.render(data_1)
    result_2 = template.render(data_2)

    assert "Special" in result_1["text"]
    assert "Regular" in result_2["text"]

# 9. Regression test to ensure simple templates still work
def test_simple_template_regression():
    body = "Hello {{ name }}"

    template = TemplateEngine(body_text=body)

    data = ExampleSchema(
        name="Legacy User",
        committee="UNDP",
        allotment="India",
        email="legacy@example.com"
    )

    result = template.render(data)

    assert result["text"] == "Hello Legacy User"
