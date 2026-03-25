"""
MCP Server Registry Explorer - Standalone Version
A complete registry manager for Model Context Protocol servers.
Simply run: python -m streamlit run app.py
"""

import streamlit as st
import json
from datetime import datetime

# ===== REGISTRY DATA (All in one file!) =====
REGISTRY_ENTRIES = [
    {
        "id": "filesystem",
        "name": "Filesystem Server",
        "category": "Data Access",
        "version": "1.0.0",
        "status": "stable",
        "description": "Read and write files on the local filesystem. Enables AI agents to interact with your file system securely.",
        "tools": [
            {
                "name": "read_file",
                "description": "Read contents of a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path to read"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write contents to a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path to write to"},
                        "contents": {"type": "string", "description": "File contents"}
                    },
                    "required": ["path", "contents"]
                }
            },
            {
                "name": "list_directory",
                "description": "List files in a directory",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path"}
                    },
                    "required": ["path"]
                }
            }
        ],
        "use_cases": [
            "Document processing and analysis",
            "Log file inspection and analysis",
            "Configuration file management",
            "Automated report generation"
        ],
        "connection_instructions": "Standard MCP connection via stdio. Configure in your agent platform's MCP settings.",
        "limitations": "File access is controlled by OS permissions. No built-in encryption.",
        "example_prompts": [
            "Read and summarize the contents of ./reports/Q1_summary.txt",
            "Create a new configuration file with these settings...",
            "List all .log files in the /var/log directory"
        ]
    },
    {
        "id": "github",
        "name": "GitHub Integration Server",
        "category": "Developer Tools",
        "version": "2.1.0",
        "status": "stable",
        "description": "Access GitHub repositories, issues, pull requests, and manage workflows. Integrate your codebase with AI-powered development.",
        "tools": [
            {
                "name": "list_repositories",
                "description": "List repositories for a GitHub user/org",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "owner": {"type": "string", "description": "Repository owner"}
                    },
                    "required": ["owner"]
                }
            },
            {
                "name": "read_file_from_repo",
                "description": "Read a file from a repository",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "repo": {"type": "string", "description": "Repository (owner/name)"},
                        "path": {"type": "string", "description": "File path"},
                        "branch": {"type": "string", "description": "Branch name"}
                    },
                    "required": ["repo", "path"]
                }
            },
            {
                "name": "list_issues",
                "description": "List issues in a repository",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "repo": {"type": "string", "description": "Repository (owner/name)"},
                        "state": {"type": "string", "enum": ["open", "closed", "all"]}
                    },
                    "required": ["repo"]
                }
            }
        ],
        "use_cases": [
            "Code review assistance",
            "Issue triaging and analysis",
            "Repository documentation generation",
            "Automated changelog creation"
        ],
        "connection_instructions": "Requires GitHub personal access token. Set GITHUB_TOKEN environment variable before starting.",
        "limitations": "Rate limited by GitHub API. Public repos only without enterprise token.",
        "example_prompts": [
            "Summarize the open issues in my repository",
            "Review this pull request for potential bugs",
            "Generate a changelog from recent commits"
        ]
    },
    {
        "id": "slack",
        "name": "Slack Integration Server",
        "category": "Communication",
        "version": "1.5.2",
        "status": "stable",
        "description": "Send messages, read channel history, and manage Slack workflows. Enable AI agents to communicate within your Slack workspace.",
        "tools": [
            {
                "name": "send_message",
                "description": "Send a message to a Slack channel",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string", "description": "Channel ID or name"},
                        "text": {"type": "string", "description": "Message text"}
                    },
                    "required": ["channel", "text"]
                }
            },
            {
                "name": "get_channel_history",
                "description": "Retrieve message history from a channel",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string", "description": "Channel ID or name"},
                        "limit": {"type": "integer", "description": "Number of messages"}
                    },
                    "required": ["channel"]
                }
            }
        ],
        "use_cases": [
            "Automated notifications and alerts",
            "Channel monitoring and analysis",
            "Daily standup summaries",
            "Incident response coordination"
        ],
        "connection_instructions": "Create a Slack Bot app and provide the Bot Token. Set SLACK_BOT_TOKEN environment variable.",
        "limitations": "Cannot delete messages. Read access limited to joined channels.",
        "example_prompts": [
            "Send a notification to #alerts about the deployment",
            "Summarize the last 20 messages in #general",
            "Post a daily standup reminder at 9 AM"
        ]
    },
    {
        "id": "database",
        "name": "SQL Database Server",
        "category": "Data Access",
        "version": "1.2.1",
        "status": "beta",
        "description": "Execute SQL queries against PostgreSQL, MySQL, or SQLite databases. Enable natural language database interactions.",
        "tools": [
            {
                "name": "execute_query",
                "description": "Execute a SQL SELECT query",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "SQL query"},
                        "database": {"type": "string", "description": "Database connection name"}
                    },
                    "required": ["query", "database"]
                }
            },
            {
                "name": "get_schema",
                "description": "Get database schema information",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "database": {"type": "string", "description": "Database name"}
                    },
                    "required": ["database"]
                }
            }
        ],
        "use_cases": [
            "Business intelligence queries",
            "Data analysis and reporting",
            "Natural language search",
            "Automated data validation"
        ],
        "connection_instructions": "Configure database credentials in config.yaml. Currently supports PostgreSQL, MySQL, and SQLite.",
        "limitations": "READ-ONLY queries only. No INSERT/UPDATE/DELETE operations for safety.",
        "example_prompts": [
            "What are our top 10 customers by revenue?",
            "Show me the monthly sales trend for Q2",
            "Find any missing values in the customer email field"
        ]
    },
    {
        "id": "web",
        "name": "Web Scraper Server",
        "category": "Data Access",
        "version": "0.9.0",
        "status": "alpha",
        "description": "Fetch and parse web content. Enable agents to gather information from websites and APIs.",
        "tools": [
            {
                "name": "fetch_url",
                "description": "Fetch content from a URL",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to fetch"},
                        "method": {"type": "string", "enum": ["GET", "POST"], "description": "HTTP method"}
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "parse_html",
                "description": "Parse HTML and extract structured data",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "html": {"type": "string", "description": "HTML content"},
                        "selector": {"type": "string", "description": "CSS selector"}
                    },
                    "required": ["html", "selector"]
                }
            }
        ],
        "use_cases": [
            "News and content aggregation",
            "Price comparison and monitoring",
            "Market research data collection",
            "API integration without native MCP server"
        ],
        "connection_instructions": "No authentication required for public URLs. For private content, configure credentials in config.yaml.",
        "limitations": "Cannot bypass authentication. May be blocked by rate limiting. Alpha status — API may change.",
        "example_prompts": [
            "What's the current Bitcoin price?",
            "Summarize the latest news from techcrunch.com",
            "Extract product prices from this e-commerce site"
        ]
    },
    {
        "id": "email",
        "name": "Email Server",
        "category": "Communication",
        "version": "1.1.0",
        "status": "stable",
        "description": "Send and receive emails. Enable agents to manage email communication and notifications.",
        "tools": [
            {
                "name": "send_email",
                "description": "Send an email",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "to": {"type": "string", "description": "Recipient email"},
                        "subject": {"type": "string", "description": "Email subject"},
                        "body": {"type": "string", "description": "Email body"},
                        "html": {"type": "boolean", "description": "Is body HTML?"}
                    },
                    "required": ["to", "subject", "body"]
                }
            },
            {
                "name": "get_inbox",
                "description": "Retrieve emails from inbox",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Number of emails"},
                        "unread_only": {"type": "boolean", "description": "Only unread emails"}
                    }
                }
            }
        ],
        "use_cases": [
            "Automated email notifications",
            "Daily digest generation",
            "Email-based workflows",
            "Customer communication automation"
        ],
        "connection_instructions": "Configure SMTP and IMAP settings in config.yaml. Supports Gmail, Outlook, and standard SMTP servers.",
        "limitations": "No attachment support yet. Requires less-secure app credentials for Gmail.",
        "example_prompts": [
            "Send a thank you email to john@example.com",
            "Read my unread emails and summarize them",
            "Create a daily digest of important emails"
        ]
    },
    {
        "id": "calendar",
        "name": "Calendar Server",
        "category": "Productivity",
        "version": "1.0.0",
        "status": "stable",
        "description": "Manage calendar events and scheduling. Enable agents to handle meetings and time management.",
        "tools": [
            {
                "name": "create_event",
                "description": "Create a calendar event",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Event title"},
                        "start_time": {"type": "string", "description": "ISO 8601 timestamp"},
                        "end_time": {"type": "string", "description": "ISO 8601 timestamp"},
                        "attendees": {"type": "array", "description": "List of attendee emails"}
                    },
                    "required": ["title", "start_time", "end_time"]
                }
            },
            {
                "name": "list_events",
                "description": "List upcoming events",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "days_ahead": {"type": "integer", "description": "Number of days to look ahead"}
                    }
                }
            }
        ],
        "use_cases": [
            "Meeting scheduling assistance",
            "Calendar insights and analytics",
            "Automated reminder generation",
            "Schedule conflict detection"
        ],
        "connection_instructions": "Supports Google Calendar and Outlook. Set CALENDAR_TOKEN environment variable with OAuth token.",
        "limitations": "Requires OAuth authorization. Cannot access other users' calendars without permission.",
        "example_prompts": [
            "Schedule a meeting with the team for next Tuesday at 2 PM",
            "What's my availability for a 1-hour meeting this week?",
            "Show me my calendar for the next 7 days"
        ]
    },
    {
        "id": "knowledgebase",
        "name": "Knowledge Base Server",
        "category": "Information Retrieval",
        "version": "2.0.1",
        "status": "stable",
        "description": "Semantic search and retrieval from your company's knowledge base. Enable agents to access documentation and corporate memory.",
        "tools": [
            {
                "name": "search_documents",
                "description": "Search knowledge base by keyword or semantic similarity",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "top_k": {"type": "integer", "description": "Number of results"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_document",
                "description": "Retrieve a specific document by ID",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "doc_id": {"type": "string", "description": "Document ID"}
                    },
                    "required": ["doc_id"]
                }
            }
        ],
        "use_cases": [
            "Employee onboarding assistance",
            "Customer support automation",
            "Policy and procedure reference",
            "Internal documentation search"
        ],
        "connection_instructions": "Index your documents using the provided indexing CLI. Supports PDF, Markdown, and plain text.",
        "limitations": "Search based on available indexed documents. New documents require re-indexing.",
        "example_prompts": [
            "What's our company's expense policy?",
            "Find documentation on the refund process",
            "Give me the onboarding checklist for new employees"
        ]
    }
]

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="MCP Server Registry Explorer",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .registry-header {
        padding: 2rem 0;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .server-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        hover_background: #f5f5f5;
        cursor: pointer;
    }
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    .status-stable {
        background-color: #d4edda;
        color: #155724;
    }
    .status-beta {
        background-color: #fff3cd;
        color: #856404;
    }
    .status-alpha {
        background-color: #f8d7da;
        color: #721c24;
    }
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        background-color: #e7f3ff;
        color: #0066cc;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ===== SESSION STATE =====
if "registry" not in st.session_state:
    st.session_state.registry = REGISTRY_ENTRIES.copy()
if "selected_server" not in st.session_state:
    st.session_state.selected_server = None

# ===== HELPER FUNCTIONS =====
def get_status_color(status):
    if status == "stable":
        return "status-stable"
    elif status == "beta":
        return "status-beta"
    else:
        return "status-alpha"

def render_server_card(server, is_selected=False):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.write(f"### {server['name']}")
        st.write(server['description'])
        col_meta1, col_meta2, col_meta3 = st.columns(3)
        with col_meta1:
            st.write(f"**Version:** {server['version']}")
        with col_meta2:
            st.write(f"**Category:** {server['category']}")
        with col_meta3:
            status_html = f"<span class='status-badge {get_status_color(server['status'])}'>{server['status'].upper()}</span>"
            st.markdown(status_html, unsafe_allow_html=True)
    with col2:
        if st.button("View Details", key=f"btn_{server['id']}", use_container_width=True):
            st.session_state.selected_server = server['id']
            st.rerun()

def render_detail_view(server):
    st.markdown(f"## {server['name']}", help=f"ID: {server['id']}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_html = f"<span class='status-badge {get_status_color(server['status'])}'>{server['status'].upper()}</span>"
        st.markdown(status_html, unsafe_allow_html=True)
    with col2:
        st.write(f"**Version:** {server['version']}")
    with col3:
        st.write(f"**Category:** {server['category']}")
    with col4:
        st.write(f"**ID:** `{server['id']}`")
    st.divider()
    st.markdown("### Description")
    st.write(server['description'])
    st.markdown("### Tools & Capabilities")
    for tool in server['tools']:
        with st.expander(f"🔧 {tool['name']}", expanded=False):
            st.write(f"**Description:** {tool['description']}")
            st.write("**Input Schema:**")
            st.json(tool['input_schema'])
    st.markdown("### Use Cases")
    for i, use_case in enumerate(server['use_cases'], 1):
        st.write(f"{i}. {use_case}")
    st.markdown("### Example Prompts")
    for prompt in server['example_prompts']:
        st.write(f"💬 _{prompt}_")
    st.markdown("### Connection Instructions")
    st.info(server['connection_instructions'])
    st.markdown("### Known Limitations")
    st.warning(server['limitations'])

def render_search_and_filter():
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input(
            "🔍 Search servers by name or description",
            placeholder="e.g., 'GitHub', 'email', 'database'",
            key="search_input"
        )
    with col2:
        categories = sorted(list(set(s['category'] for s in st.session_state.registry)))
        selected_category = st.selectbox(
            "📁 Filter by Category",
            ["All Categories"] + categories,
            key="category_filter"
        )
    return search_query, selected_category

def filter_registry(search_query, category_filter):
    filtered = st.session_state.registry
    if search_query:
        search_lower = search_query.lower()
        filtered = [
            s for s in filtered
            if search_lower in s['name'].lower() or search_lower in s['description'].lower()
        ]
    if category_filter != "All Categories":
        filtered = [s for s in filtered if s['category'] == category_filter]
    return filtered

def add_new_entry():
    st.markdown("## Add New MCP Server Entry")
    with st.form("new_entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Server Name *", placeholder="e.g., Slack Integration Server")
            server_id = st.text_input("Server ID *", placeholder="e.g., slack (lowercase, no spaces)")
        with col2:
            version = st.text_input("Version *", placeholder="e.g., 1.0.0", value="1.0.0")
            category = st.selectbox(
                "Category *",
                ["Data Access", "Developer Tools", "Communication", "Productivity", "Information Retrieval", "Other"]
            )
        description = st.text_area(
            "Description *",
            placeholder="What does this MCP server do?",
            height=80
        )
        status = st.radio(
            "Status",
            ["stable", "beta", "alpha"],
            horizontal=True,
            index=0
        )
        use_cases_text = st.text_area(
            "Use Cases (one per line)",
            placeholder="Automated notifications\nChannel monitoring\nDaily reports",
            height=60
        )
        connection_instructions = st.text_area(
            "Connection Instructions",
            placeholder="Setup steps and configuration details...",
            height=60
        )
        limitations = st.text_area(
            "Known Limitations",
            placeholder="Current limitations or constraints...",
            height=60
        )
        example_prompts_text = st.text_area(
            "Example Prompts (one per line)",
            placeholder="Send a notification to #alerts\nSummarize the channel\nPost a reminder",
            height=60
        )
        submitted = st.form_submit_button("✨ Add to Registry", use_container_width=True)
        if submitted:
            if not all([name, server_id, description]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                use_cases = [uc.strip() for uc in use_cases_text.split('\n') if uc.strip()]
                example_prompts = [ep.strip() for ep in example_prompts_text.split('\n') if ep.strip()]
                new_entry = {
                    "id": server_id.lower(),
                    "name": name,
                    "category": category,
                    "version": version,
                    "status": status,
                    "description": description,
                    "tools": [],
                    "use_cases": use_cases if use_cases else ["General purpose"],
                    "connection_instructions": connection_instructions or "Configure as needed.",
                    "limitations": limitations or "None documented.",
                    "example_prompts": example_prompts if example_prompts else ["Example usage"]
                }
                st.session_state.registry.append(new_entry)
                st.success(f"✅ Successfully added '{name}' to the registry!")
                st.balloons()

# ===== MAIN APP =====
def main():
    st.sidebar.markdown("# 🗂️ MCP Registry Explorer")
    page = st.sidebar.radio(
        "Navigation",
        ["Browse Registry", "Add New Entry"],
        key="nav_radio"
    )
    
    if st.session_state.selected_server:
        if st.sidebar.button("← Back to List", use_container_width=True):
            st.session_state.selected_server = None
            st.rerun()
    
    st.sidebar.divider()
    st.sidebar.markdown("### Registry Stats")
    col_stats1, col_stats2 = st.sidebar.columns(2)
    with col_stats1:
        st.metric("Total Servers", len(st.session_state.registry))
    with col_stats2:
        stable_count = sum(1 for s in st.session_state.registry if s['status'] == 'stable')
        st.metric("Stable", stable_count)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("🚀 MCP Server Registry Explorer v1.0.0\nBuild your AI agent toolkit")
    
    if st.session_state.selected_server:
        selected_server = next(
            (s for s in st.session_state.registry if s['id'] == st.session_state.selected_server),
            None
        )
        if selected_server:
            render_detail_view(selected_server)
    else:
        if page == "Browse Registry":
            st.markdown("""
                <div class="registry-header">
                    <h1>🗂️ MCP Server Registry</h1>
                    <p>Discover, explore, and manage AI Model Context Protocol servers</p>
                </div>
            """, unsafe_allow_html=True)
            search_query, category_filter = render_search_and_filter()
            filtered_registry = filter_registry(search_query, category_filter)
            if filtered_registry:
                st.write(f"**Found {len(filtered_registry)} server(s)**")
                st.divider()
                for server in filtered_registry:
                    render_server_card(server)
            else:
                st.info("No servers found matching your criteria. Try adjusting your search or filter.")
        else:
            add_new_entry()

if __name__ == "__main__":
    main()
