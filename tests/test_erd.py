from sfdata_schema.docgen.erd import get_erd_context, graphviz_render_erd, render_erd


def test_get_erd_context(pet_schema):
    context = get_erd_context(pet_schema)
    assert context["schema"] == pet_schema

    relationships = context["relationships"]
    assert len(relationships) == 3

    rel_map = {rel.lh: rel for rel in relationships}

    assert rel_map["pet"].lh == "pet"
    assert rel_map["pet"].rh == "person"
    assert rel_map["pet"].lh_c == "0..N"

    assert rel_map["address"].lh == "address"
    assert rel_map["address"].rh == "person"
    assert rel_map["address"].lh_c == "0..N"

    assert rel_map["primary_phone"].lh == "primary_phone"
    assert rel_map["primary_phone"].rh == "person"
    assert rel_map["primary_phone"].lh_c == "0,1"


def test_render_erd(pet_schema):
    erd = render_erd(pet_schema)
    assert '<TD COLSPAN="3"><B><FONT POINT-SIZE="16">person</FONT></B></TD>' in erd
    assert '<TD ALIGN="LEFT">first_name</TD>'


def test_dot_save(pet_schema, dist_dir):
    png_path = dist_dir / "test_dot.png"
    svg_path = dist_dir / "test_dot.svg"

    graphviz_render_erd(pet_schema, "png", png_path)
    graphviz_render_erd(pet_schema, "svg", svg_path)


def test_dot_svg(pet_schema):
    svg_bytes = graphviz_render_erd(pet_schema, "svg")
    svg = svg_bytes.decode("utf-8")

    assert "<title>person</title>" in svg
    assert "<title>pet</title>" in svg
    assert "<title>address</title>" in svg
    assert '<polygon fill="LightPink"' in svg
