import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, _dash_renderer, dcc, callback, Input, Output, State

_dash_renderer._set_react_version("18.2.0")


theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    color="yellow",
    id="color-scheme-toggle",
    size="lg",
    ms="auto",
)

header = dmc.Group(
    [
        dmc.Burger(id="burger-button", opened=False, hiddenFrom="md"),
        dmc.Text(["Header"], size="xl", fw=700),
        theme_toggle
    ],
    justify="flex-start",
)

navbar = dcc.Loading(
    dmc.ScrollArea(
        [
            dmc.Text("Your Sidebar content", fw=700),
        ],
        offsetScrollbars=True,
        type="scroll",
        style={"height": "100%"},
    ),
)

page_content = [dmc.Text("Your page content"), dmc.Loader(color="red", size="md", variant="oval")]

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

app = Dash(external_stylesheets=stylesheets)


app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, px=25),
        dmc.AppShellNavbar(navbar, p=24),
        dmc.AppShellAside("Aside", withBorder=False),
        dmc.AppShellMain(page_content),
        dmc.AppShellFooter("Footer")
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 375,
        "breakpoint": "md",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 300,
        "breakpoint": "xl",
        "collapsed": {"desktop": False, "mobile": True},
    },
    id="app-shell",
)

app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        app_shell
    ],
    id="mantine-provider",
    forceColorScheme="light",
)


@callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    return "dark" if theme == "light" else "light"



if __name__ == "__main__":
    app.run_server(debug=True, port=8051)