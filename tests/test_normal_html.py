"""Test readability.py on sample articles"""
from .checks import check_exact_html_output, check_html_output_contains_text

# Test bare text behaviours
def test_html_bare_text():
    """Bare text should be wrapped in <p> tags."""
    check_html_output_contains_text(
        "Bare text here",
        "<p>Bare text here</p>"
    )


def test_html_bare_text_linebreaks():
    """Line breaks in bare text should be removed."""
    check_html_output_contains_text("""
        Bare text with
        some linebreaks here
    """, "<p>Bare text with some linebreaks here</p>")


def test_html_bare_text_double_br():
    """Double <br> in bare text should trigger a new paragraph."""
    check_html_output_contains_text("""
        Bare text with
        <br/><br/>
        some linebreaks here
    """, "<p>Bare text with</p><p>some linebreaks here</p>")


def test_html_space_separated_double_br():
    """Double <br> separated by whitespace should still trigger a new paragraph."""
    check_html_output_contains_text("""
        Bare text with
        <br/>
               <br/>
        some linebreaks here
    """, "<p>Bare text with</p><p>some linebreaks here</p>")


def test_html_space_separated_double_br_inside_div():
    """Double <br> separated by whitespace should still trigger a new div."""
    check_html_output_contains_text("""
        <div>
            Text with
            <br/>
                <br/>
            some linebreaks here
        <div>
    """, "<div><p>Text with</p><p>some linebreaks here</p></div>")


# Test correct wrapping
def test_ensure_correct_div_wrapping():
    """Do not wrap in a <div> if this is already a <div>."""
    check_exact_html_output("""
        <div>
            <p>
                Some example text here.
            </p>
        </div>""",
    """<div><p>Some example text here.</p></div>""")


# Test consecutive links
def test_consecutive_links():
    """Do not wrap in a <div> if this is already a <div>."""
    check_exact_html_output("""
        <blockquote>
			<p>First paragraph <a href="https://example.com">first link</a> <a href="https://example.com">second link</a></p>
			<p>Second paragraph: <a href="https://example.com">third link</a></p>
		</blockquote>""",
    "<div><blockquote><p>First paragraph first link second link</p><p>Second paragraph: third link</p></blockquote></div>")


# Test text consolidation
def test_span_removal_and_conversion():
    """First <span> should be removed. Second should give bare text that will be wrapped."""
    check_exact_html_output("""
        <div>
            <p>Some <span>example</span> text here.</p>
            <span>More text in a span.</span>
        </div>""",
    """<div><p>Some example text here.</p><p>More text in a span.</p></div>""")


def test_consolidating_string_between_tags():
    """First <span> should be removed. Second should give bare text that will be wrapped."""
    check_exact_html_output("""
        <div>
            <p>Some <br><br>example text here.</p>
            <span>More text in a span.</span>
            Part of the same paragraph. <br>
            <br> A new paragraph.
        </div>""",
    """<div><p>Some</p><p>example text here.</p><p>More text in a span. Part of the same paragraph.</p><p>A new paragraph.</p></div>""")


# def test_bare_text_wrapping():
#     """First <span> should be removed. Second should give bare text that will be wrapped."""
#     check_exact_html_output("""
#         <div>
#             <p>Some <br/><br/>example text here.</p>
#             Bare text. <br/>
#             <br/> A new paragraph.
#         </div>""",
#     """<div><p>Some example text here.</p><p>More text in a span. Part of the same paragraph.</p><p>A new paragraph.</p></div>""")