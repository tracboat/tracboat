# -*- coding: utf-8 -*-

from peewee import *
from playhouse.postgres_ext import *

database_proxy = Proxy()

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database_proxy

class AbuseReports(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    message = TextField(null=True)
    message_html = TextField(null=True)
    reporter = IntegerField(db_column='reporter_id', null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'abuse_reports'

class Appearances(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField()
    description = TextField()
    description_html = TextField(null=True)
    email_header_and_footer_enabled = BooleanField()
    favicon = CharField(null=True)
    footer_message = TextField(null=True)
    footer_message_html = TextField(null=True)
    header_logo = CharField(null=True)
    header_message = TextField(null=True)
    header_message_html = TextField(null=True)
    logo = CharField(null=True)
    message_background_color = TextField(null=True)
    message_font_color = TextField(null=True)
    new_project_guidelines = TextField(null=True)
    new_project_guidelines_html = TextField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        db_table = 'appearances'

class ApplicationSettingTerms(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    terms = TextField()
    terms_html = TextField(null=True)

    class Meta:
        db_table = 'application_setting_terms'

class Users(BaseModel):
    accepted_term = ForeignKeyField(db_column='accepted_term_id', null=True, rel_model=ApplicationSettingTerms, to_field='id')
    admin = BooleanField(index=True)
    avatar = CharField(null=True)
    bio = CharField(null=True)
    can_create_group = BooleanField()
    can_create_team = BooleanField()
    color_scheme = IntegerField(db_column='color_scheme_id')
    commit_email = CharField(null=True)
    confirmation_sent_at = DateTimeField(null=True)
    confirmation_token = CharField(null=True, unique=True)
    confirmed_at = DateTimeField(null=True)
    consumed_timestep = IntegerField(null=True)
    created_at = DateTimeField(index=True, null=True)
    created_by = IntegerField(db_column='created_by_id', null=True)
    current_sign_in_at = DateTimeField(null=True)
    current_sign_in_ip = CharField(null=True)
    dashboard = IntegerField(null=True)
    email = CharField(index=True)
    encrypted_otp_secret = CharField(null=True)
    encrypted_otp_secret_iv = CharField(null=True)
    encrypted_otp_secret_salt = CharField(null=True)
    encrypted_password = CharField()
    external = BooleanField(null=True)
    failed_attempts = IntegerField(null=True)
    feed_token = CharField(index=True, null=True)
    ghost = BooleanField(index=True, null=True)
    hide_no_password = BooleanField(null=True)
    hide_no_ssh_key = BooleanField(null=True)
    hide_project_limit = BooleanField(null=True)
    include_private_contributions = BooleanField(null=True)
    incoming_email_token = CharField(index=True, null=True)
    last_activity_on = DateField(null=True)
    last_credential_check_at = DateTimeField(null=True)
    last_sign_in_at = DateTimeField(null=True)
    last_sign_in_ip = CharField(null=True)
    layout = IntegerField(null=True)
    linkedin = CharField()
    location = CharField(null=True)
    locked_at = DateTimeField(null=True)
    name = CharField(index=True, null=True)
    notification_email = CharField(null=True)
    notified_of_own_activity = BooleanField(null=True)
    organization = CharField(null=True)
    otp_backup_codes = TextField(null=True)
    otp_grace_period_started_at = DateTimeField(null=True)
    otp_required_for_login = BooleanField()
    password_automatically_set = BooleanField(null=True)
    password_expires_at = DateTimeField(null=True)
    preferred_language = CharField(null=True)
    private_profile = BooleanField(null=True)
    project_view = IntegerField(null=True)
    projects_limit = IntegerField()
    public_email = CharField()
    remember_created_at = DateTimeField(null=True)
    require_two_factor_authentication_from_group = BooleanField()
    reset_password_sent_at = DateTimeField(null=True)
    reset_password_token = CharField(null=True, unique=True)
    sign_in_count = IntegerField(null=True)
    skype = CharField()
    state = CharField(index=True, null=True)
    theme = IntegerField(db_column='theme_id', null=True)
    twitter = CharField()
    two_factor_grace_period = IntegerField()
    unconfirmed_email = CharField(null=True)
    unlock_token = CharField(null=True)
    updated_at = DateTimeField(null=True)
    username = CharField(index=True, null=True)
    website_url = CharField()

    class Meta:
        db_table = 'users'

class ApplicationSettings(BaseModel):
    admin_notification_email = CharField(null=True)
    after_sign_out_path = CharField(null=True)
    after_sign_up_text = TextField(null=True)
    after_sign_up_text_html = TextField(null=True)
    akismet_api_key = CharField(null=True)
    akismet_enabled = BooleanField(null=True)
    allow_local_requests_from_hooks_and_services = BooleanField()
    archive_builds_in_seconds = IntegerField(null=True)
    authorized_keys_enabled = BooleanField()
    auto_devops_domain = CharField(null=True)
    auto_devops_enabled = BooleanField()
    cached_markdown_version = IntegerField(null=True)
    clientside_sentry_dsn = CharField(null=True)
    clientside_sentry_enabled = BooleanField()
    commit_email_hostname = CharField(null=True)
    container_registry_token_expire_delay = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    default_artifacts_expire_in = CharField()
    default_branch_protection = IntegerField(null=True)
    default_group_visibility = IntegerField(null=True)
    default_project_creation = IntegerField()
    default_project_visibility = IntegerField(null=True)
    default_projects_limit = IntegerField(null=True)
    default_snippet_visibility = IntegerField(null=True)
    diff_max_patch_bytes = IntegerField()
    disabled_oauth_sign_in_sources = TextField(null=True)
    domain_blacklist = TextField(null=True)
    domain_blacklist_enabled = BooleanField(null=True)
    domain_whitelist = TextField(null=True)
    dsa_key_restriction = IntegerField()
    ecdsa_key_restriction = IntegerField()
    ed25519_key_restriction = IntegerField()
    email_author_in_body = BooleanField(null=True)
    enabled_git_access_protocol = CharField(null=True)
    encrypted_external_auth_client_key = TextField(null=True)
    encrypted_external_auth_client_key_iv = CharField(null=True)
    encrypted_external_auth_client_key_pass = CharField(null=True)
    encrypted_external_auth_client_key_pass_iv = CharField(null=True)
    enforce_terms = BooleanField(null=True)
    external_auth_client_cert = TextField(null=True)
    external_authorization_service_default_label = CharField(null=True)
    external_authorization_service_enabled = BooleanField()
    external_authorization_service_timeout = FloatField(null=True)
    external_authorization_service_url = CharField(null=True)
    first_day_of_week = IntegerField()
    gitaly_timeout_default = IntegerField()
    gitaly_timeout_fast = IntegerField()
    gitaly_timeout_medium = IntegerField()
    gravatar_enabled = BooleanField(null=True)
    hashed_storage_enabled = BooleanField()
    health_check_access_token = CharField(null=True)
    help_page_hide_commercial_content = BooleanField(null=True)
    help_page_support_url = CharField(null=True)
    help_page_text = TextField(null=True)
    help_page_text_html = TextField(null=True)
    hide_third_party_offers = BooleanField()
    home_page_url = CharField(null=True)
    housekeeping_bitmaps_enabled = BooleanField()
    housekeeping_enabled = BooleanField()
    housekeeping_full_repack_period = IntegerField()
    housekeeping_gc_period = IntegerField()
    housekeeping_incremental_repack_period = IntegerField()
    html_emails_enabled = BooleanField(null=True)
    import_sources = TextField(null=True)
    instance_statistics_visibility_private = BooleanField()
    local_markdown_version = IntegerField()
    max_artifacts_size = IntegerField()
    max_attachment_size = IntegerField()
    max_pages_size = IntegerField()
    metrics_enabled = BooleanField(null=True)
    metrics_host = CharField(null=True)
    metrics_method_call_threshold = IntegerField(null=True)
    metrics_packet_size = IntegerField(null=True)
    metrics_pool_size = IntegerField(null=True)
    metrics_port = IntegerField(null=True)
    metrics_sample_interval = IntegerField(null=True)
    metrics_timeout = IntegerField(null=True)
    mirror_available = BooleanField()
    pages_domain_verification_enabled = BooleanField()
    password_authentication_enabled_for_git = BooleanField()
    password_authentication_enabled_for_web = BooleanField(null=True)
    performance_bar_allowed_group = IntegerField(db_column='performance_bar_allowed_group_id', null=True)
    plantuml_enabled = BooleanField(null=True)
    plantuml_url = CharField(null=True)
    polling_interval_multiplier = DecimalField()
    project_export_enabled = BooleanField()
    prometheus_metrics_enabled = BooleanField()
    protected_ci_variables = BooleanField()
    recaptcha_enabled = BooleanField(null=True)
    recaptcha_private_key = CharField(null=True)
    recaptcha_site_key = CharField(null=True)
    receive_max_input_size = IntegerField(null=True)
    repository_checks_enabled = BooleanField(null=True)
    repository_storages = CharField(null=True)
    require_two_factor_authentication = BooleanField(null=True)
    restricted_visibility_levels = TextField(null=True)
    rsa_key_restriction = IntegerField()
    runners_registration_token = CharField(null=True)
    runners_registration_token_encrypted = CharField(null=True)
    send_user_confirmation_email = BooleanField(null=True)
    sentry_dsn = CharField(null=True)
    sentry_enabled = BooleanField(null=True)
    session_expire_delay = IntegerField()
    shared_runners_enabled = BooleanField()
    shared_runners_text = TextField(null=True)
    shared_runners_text_html = TextField(null=True)
    sign_in_text = TextField(null=True)
    sign_in_text_html = TextField(null=True)
    signup_enabled = BooleanField(null=True)
    terminal_max_session_time = IntegerField()
    throttle_authenticated_api_enabled = BooleanField()
    throttle_authenticated_api_period_in_seconds = IntegerField()
    throttle_authenticated_api_requests_per_period = IntegerField()
    throttle_authenticated_web_enabled = BooleanField()
    throttle_authenticated_web_period_in_seconds = IntegerField()
    throttle_authenticated_web_requests_per_period = IntegerField()
    throttle_unauthenticated_enabled = BooleanField()
    throttle_unauthenticated_period_in_seconds = IntegerField()
    throttle_unauthenticated_requests_per_period = IntegerField()
    two_factor_grace_period = IntegerField(null=True)
    unique_ips_limit_enabled = BooleanField()
    unique_ips_limit_per_user = IntegerField(null=True)
    unique_ips_limit_time_window = IntegerField(null=True)
    updated_at = DateTimeField(null=True)
    usage_ping_enabled = BooleanField()
    usage_stats_set_by_user = ForeignKeyField(db_column='usage_stats_set_by_user_id', null=True, rel_model=Users, to_field='id')
    user_default_external = BooleanField()
    user_default_internal_regex = CharField(null=True)
    user_oauth_applications = BooleanField(null=True)
    user_show_add_ssh_key_message = BooleanField()
    uuid = CharField(null=True)
    version_check_enabled = BooleanField(null=True)
    web_ide_clientside_preview_enabled = BooleanField()

    class Meta:
        db_table = 'application_settings'

class ArInternalMetadata(BaseModel):
    created_at = DateTimeField()
    key = CharField(primary_key=True)
    updated_at = DateTimeField()
    value = CharField(null=True)

    class Meta:
        db_table = 'ar_internal_metadata'

class AuditEvents(BaseModel):
    author = IntegerField(db_column='author_id')
    created_at = DateTimeField(null=True)
    details = TextField(null=True)
    entity = IntegerField(db_column='entity_id')
    entity_type = CharField()
    type = CharField()
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'audit_events'
        indexes = (
            (('entity', 'entity_type'), False),
        )

class AwardEmoji(BaseModel):
    awardable = IntegerField(db_column='awardable_id', null=True)
    awardable_type = CharField(null=True)
    created_at = DateTimeField(null=True)
    name = CharField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'award_emoji'
        indexes = (
            (('awardable', 'awardable_type'), False),
            (('name', 'user'), False),
        )

class Namespaces(BaseModel):
    auto_devops_enabled = BooleanField(null=True)
    avatar = CharField(null=True)
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField(index=True, null=True)
    description = CharField()
    description_html = TextField(null=True)
    lfs_enabled = BooleanField(null=True)
    name = CharField(index=True)
    owner = IntegerField(db_column='owner_id', index=True, null=True)
    parent = IntegerField(db_column='parent_id', null=True)
    path = CharField(index=True)
    project_creation_level = IntegerField(null=True)
    request_access_enabled = BooleanField()
    require_two_factor_authentication = BooleanField(index=True)
    runners_token = CharField(null=True, unique=True)
    runners_token_encrypted = CharField(null=True, unique=True)
    share_with_group_lock = BooleanField(null=True)
    two_factor_grace_period = IntegerField()
    type = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    visibility_level = IntegerField()

    class Meta:
        db_table = 'namespaces'
        indexes = (
            (('id', 'parent'), True),
            (('parent', 'name'), True),
        )

# Possible reference cycle: projects
class Shards(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'shards'

class PoolRepositories(BaseModel):
    disk_path = CharField(null=True, unique=True)
    id = BigIntegerField(primary_key=True)
    shard = ForeignKeyField(db_column='shard_id', rel_model=Shards, to_field='id')
    source_project = ForeignKeyField(db_column='source_project_id', null=True, rel_model=Projects, to_field='id', unique=True)
    state = CharField(null=True)

    class Meta:
        db_table = 'pool_repositories'

class Projects(BaseModel):
    archived = BooleanField()
    auto_cancel_pending_pipelines = IntegerField()
    avatar = CharField(null=True)
    bfg_object_map = CharField(null=True)
    build_allow_git_fetch = BooleanField()
    build_coverage_regex = CharField(null=True)
    build_timeout = IntegerField()
    cached_markdown_version = IntegerField(null=True)
    ci_config_path = CharField(null=True)
    ci = IntegerField(db_column='ci_id', index=True, null=True)
    container_registry_enabled = BooleanField(null=True)
    created_at = DateTimeField(index=True, null=True)
    creator = IntegerField(db_column='creator_id', index=True, null=True)
    delete_error = TextField(null=True)
    description = TextField(index=True, null=True)
    description_html = TextField(null=True)
    detected_repository_languages = BooleanField(null=True)
    external_authorization_classification_label = CharField(null=True)
    has_external_issue_tracker = BooleanField(null=True)
    has_external_wiki = BooleanField(null=True)
    import_error = TextField(null=True)
    import_jid = CharField(null=True)
    import_source = CharField(null=True)
    import_status = CharField(null=True)
    import_type = CharField(null=True)
    import_url = CharField(null=True)
    jobs_cache_index = IntegerField(null=True)
    last_activity_at = DateTimeField(index=True, null=True)
    last_repository_check_at = DateTimeField(index=True, null=True)
    last_repository_check_failed = BooleanField(index=True, null=True)
    last_repository_updated_at = DateTimeField(index=True, null=True)
    lfs_enabled = BooleanField(null=True)
    merge_requests_ff_only_enabled = BooleanField()
    merge_requests_rebase_enabled = BooleanField()
    name = CharField(index=True, null=True)
    namespace = IntegerField(db_column='namespace_id', index=True)
    only_allow_merge_if_all_discussions_are_resolved = BooleanField(null=True)
    only_allow_merge_if_pipeline_succeeds = BooleanField()
    pages_https_only = BooleanField(null=True)
    path = CharField(index=True, null=True)
    pending_delete = BooleanField(index=True, null=True)
    pool_repository = ForeignKeyField(db_column='pool_repository_id', null=True, rel_model=PoolRepositories, to_field='id')
    printing_merge_request_link_enabled = BooleanField()
    public_builds = BooleanField()
    remote_mirror_available_overridden = BooleanField(null=True)
    repository_read_only = BooleanField(null=True)
    repository_storage = CharField(index=True)
    request_access_enabled = BooleanField()
    resolve_outdated_diff_discussions = BooleanField(null=True)
    runners_token = CharField(index=True, null=True)
    runners_token_encrypted = CharField(index=True, null=True)
    shared_runners_enabled = BooleanField()
    star_count = IntegerField(index=True)
    storage_version = IntegerField(null=True)
    updated_at = DateTimeField(null=True)
    visibility_level = IntegerField(index=True)

    class Meta:
        db_table = 'projects'
        indexes = (
            (('repository_storage', 'created_at'), False),
        )

class Badges(BaseModel):
    created_at = DateTimeField()
    group = ForeignKeyField(db_column='group_id', null=True, rel_model=Namespaces, to_field='id')
    image_url = CharField()
    link_url = CharField()
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        db_table = 'badges'

class Boards(BaseModel):
    created_at = DateTimeField()
    group = ForeignKeyField(db_column='group_id', null=True, rel_model=Namespaces, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'boards'

class BoardGroupRecentVisits(BaseModel):
    board = ForeignKeyField(db_column='board_id', null=True, rel_model=Boards, to_field='id')
    created_at = DateTimeField()
    group = ForeignKeyField(db_column='group_id', null=True, rel_model=Namespaces, to_field='id')
    id = BigIntegerField(primary_key=True)
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'board_group_recent_visits'
        indexes = (
            (('board', 'group', 'user'), True),
        )

class BoardProjectRecentVisits(BaseModel):
    board = ForeignKeyField(db_column='board_id', null=True, rel_model=Boards, to_field='id')
    created_at = DateTimeField()
    id = BigIntegerField(primary_key=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'board_project_recent_visits'
        indexes = (
            (('project', 'board', 'user'), True),
        )

class BroadcastMessages(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    color = CharField(null=True)
    created_at = DateTimeField()
    ends_at = DateTimeField()
    font = CharField(null=True)
    message = TextField()
    message_html = TextField()
    starts_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        db_table = 'broadcast_messages'
        indexes = (
            (('id', 'starts_at', 'ends_at'), False),
        )

class ChatNames(BaseModel):
    chat = CharField(db_column='chat_id')
    chat_name = CharField(null=True)
    created_at = DateTimeField()
    last_used_at = DateTimeField(null=True)
    service = IntegerField(db_column='service_id')
    team_domain = CharField(null=True)
    team = CharField(db_column='team_id')
    updated_at = DateTimeField()
    user = IntegerField(db_column='user_id')

    class Meta:
        db_table = 'chat_names'
        indexes = (
            (('service', 'team', 'chat'), True),
            (('user', 'service'), True),
        )

class ChatTeams(BaseModel):
    created_at = DateTimeField()
    name = CharField(null=True)
    namespace = ForeignKeyField(db_column='namespace_id', rel_model=Namespaces, to_field='id', unique=True)
    team = CharField(db_column='team_id', null=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'chat_teams'

# Possible reference cycle: ci_pipelines
# Possible reference cycle: merge_requests
class MergeRequestDiffs(BaseModel):
    base_commit_sha = CharField(null=True)
    commits_count = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    external_diff = CharField(null=True)
    external_diff_store = IntegerField(null=True)
    head_commit_sha = CharField(null=True)
    merge_request = ForeignKeyField(db_column='merge_request_id', rel_model=MergeRequests, to_field='id')
    real_size = CharField(null=True)
    start_commit_sha = CharField(null=True)
    state = CharField(null=True)
    stored_externally = BooleanField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'merge_request_diffs'
        indexes = (
            (('id', 'merge_request'), False),
            (('id', 'merge_request'), False),
        )

class Milestones(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    description = TextField(index=True, null=True)
    description_html = TextField(null=True)
    due_date = DateField(index=True, null=True)
    group = ForeignKeyField(db_column='group_id', null=True, rel_model=Namespaces, to_field='id')
    iid = IntegerField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    start_date = DateField(null=True)
    state = CharField(null=True)
    title = CharField(index=True)
    title_html = TextField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'milestones'
        indexes = (
            (('project', 'iid'), True),
        )

class MergeRequests(BaseModel):
    allow_maintainer_to_push = BooleanField(null=True)
    assignee = ForeignKeyField(db_column='assignee_id', null=True, rel_model=Users, to_field='id')
    author = ForeignKeyField(db_column='author_id', null=True, rel_model=Users, related_name='users_author_set', to_field='id')
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField(index=True, null=True)
    description = TextField(index=True, null=True)
    description_html = TextField(null=True)
    discussion_locked = BooleanField(null=True)
    head_pipeline = ForeignKeyField(db_column='head_pipeline_id', null=True, rel_model=CiPipelines, to_field='id')
    iid = IntegerField(null=True)
    in_progress_merge_commit_sha = CharField(null=True)
    last_edited_at = DateTimeField(null=True)
    last_edited_by = IntegerField(db_column='last_edited_by_id', null=True)
    latest_merge_request_diff = ForeignKeyField(db_column='latest_merge_request_diff_id', null=True, rel_model=MergeRequestDiffs, to_field='id')
    lock_version = IntegerField(null=True)
    merge_commit_sha = CharField(null=True)
    merge_error = TextField(null=True)
    merge_jid = CharField(null=True)
    merge_params = TextField(null=True)
    merge_status = CharField()
    merge_user = ForeignKeyField(db_column='merge_user_id', null=True, rel_model=Users, related_name='users_merge_user_set', to_field='id')
    merge_when_pipeline_succeeds = BooleanField()
    milestone = ForeignKeyField(db_column='milestone_id', null=True, rel_model=Milestones, to_field='id')
    rebase_commit_sha = CharField(null=True)
    source_branch = CharField(index=True)
    source_project = ForeignKeyField(db_column='source_project_id', null=True, rel_model=Projects, to_field='id')
    squash = BooleanField()
    state = CharField()
    state_id = IntegerField(null=True)
    target_branch = CharField(index=True)
    target_project = ForeignKeyField(db_column='target_project_id', rel_model=Projects, related_name='projects_target_project_set', to_field='id')
    time_estimate = IntegerField(null=True)
    title = CharField(index=True, null=True)
    title_html = TextField(null=True)
    updated_at = DateTimeField(null=True)
    updated_by = ForeignKeyField(db_column='updated_by_id', null=True, rel_model=Users, related_name='users_updated_by_set', to_field='id')

    class Meta:
        db_table = 'merge_requests'
        indexes = (
            (('id', 'merge_jid'), False),
            (('source_branch', 'source_project'), False),
            (('source_project', 'source_branch'), False),
            (('target_project', 'iid'), False),
            (('target_project', 'iid'), True),
            (('target_project', 'merge_commit_sha', 'id'), False),
        )

class CiPipelineSchedules(BaseModel):
    active = BooleanField(null=True)
    created_at = DateTimeField(null=True)
    cron = CharField(null=True)
    cron_timezone = CharField(null=True)
    description = CharField(null=True)
    next_run_at = DateTimeField(null=True)
    owner = ForeignKeyField(db_column='owner_id', null=True, rel_model=Users, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    ref = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_pipeline_schedules'
        indexes = (
            (('next_run_at', 'active'), False),
        )

class CiPipelines(BaseModel):
    auto_canceled_by = ForeignKeyField(db_column='auto_canceled_by_id', null=True, rel_model='self', to_field='id')
    before_sha = CharField(null=True)
    committed_at = DateTimeField(null=True)
    config_source = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    duration = IntegerField(null=True)
    failure_reason = IntegerField(null=True)
    finished_at = DateTimeField(null=True)
    iid = IntegerField(null=True)
    lock_version = IntegerField(null=True)
    merge_request = ForeignKeyField(db_column='merge_request_id', null=True, rel_model=MergeRequests, to_field='id')
    pipeline_schedule = ForeignKeyField(db_column='pipeline_schedule_id', null=True, rel_model=CiPipelineSchedules, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    protected = BooleanField(null=True)
    ref = CharField(null=True)
    sha = CharField(null=True)
    source = IntegerField(null=True)
    source_sha = BlobField(null=True)
    started_at = DateTimeField(null=True)
    status = CharField(index=True, null=True)
    tag = BooleanField(null=True)
    target_sha = BlobField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)
    yaml_errors = TextField(null=True)

    class Meta:
        db_table = 'ci_pipelines'
        indexes = (
            (('config_source', 'status', 'project'), False),
            (('id', 'project', 'ref'), False),
            (('id', 'ref', 'project', 'status'), False),
            (('iid', 'project'), True),
            (('project', 'sha'), False),
            (('source', 'project'), False),
        )

class CiStages(BaseModel):
    created_at = DateTimeField(null=True)
    lock_version = IntegerField(null=True)
    name = CharField(null=True)
    pipeline = ForeignKeyField(db_column='pipeline_id', null=True, rel_model=CiPipelines, to_field='id')
    position = IntegerField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    status = IntegerField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_stages'
        indexes = (
            (('pipeline', 'name'), True),
            (('pipeline', 'position'), False),
        )

class CiBuilds(BaseModel):
    allow_failure = BooleanField()
    artifacts_expire_at = DateTimeField(index=True, null=True)
    artifacts_file = TextField(null=True)
    artifacts_file_store = IntegerField(null=True)
    artifacts_metadata = TextField(null=True)
    artifacts_metadata_store = IntegerField(null=True)
    artifacts_size = BigIntegerField(null=True)
    auto_canceled_by = ForeignKeyField(db_column='auto_canceled_by_id', null=True, rel_model=CiPipelines, to_field='id')
    commands = TextField(null=True)
    commit = ForeignKeyField(db_column='commit_id', null=True, rel_model=CiPipelines, related_name='ci_pipelines_commit_set', to_field='id')
    coverage = FloatField(null=True)
    coverage_regex = CharField(null=True)
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    environment = CharField(null=True)
    erased_at = DateTimeField(null=True)
    erased_by = IntegerField(db_column='erased_by_id', null=True)
    failure_reason = IntegerField(null=True)
    finished_at = DateTimeField(null=True)
    lock_version = IntegerField(null=True)
    name = CharField(null=True)
    options = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    protected = BooleanField(index=True, null=True)
    queued_at = DateTimeField(null=True)
    ref = CharField(null=True)
    retried = BooleanField(null=True)
    runner = IntegerField(db_column='runner_id', index=True, null=True)
    scheduled_at = DateTimeField(index=True, null=True)
    stage = CharField(null=True)
    stage_id = ForeignKeyField(db_column='stage_id', null=True, rel_model=CiStages, to_field='id')
    stage_idx = IntegerField(null=True)
    started_at = DateTimeField(null=True)
    status = CharField(null=True)
    tag = BooleanField(null=True)
    target_url = CharField(null=True)
    token = CharField(null=True, unique=True)
    token_encrypted = CharField(null=True, unique=True)
    trace = TextField(null=True)
    trigger_request = IntegerField(db_column='trigger_request_id', null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(index=True, null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)
    when = CharField(null=True)
    yaml_variables = TextField(null=True)

    class Meta:
        db_table = 'ci_builds'
        indexes = (
            (('commit', 'created_at', 'stage_idx'), False),
            (('commit', 'type', 'ref'), False),
            (('id', 'commit', 'artifacts_expire_at'), False),
            (('project', 'id'), False),
            (('stage_idx', 'stage_id'), False),
            (('status', 'project'), False),
            (('status', 'runner', 'type'), False),
            (('type', 'ref', 'name', 'commit'), False),
            (('type', 'status', 'commit'), False),
        )

class CiBuildTraceChunks(BaseModel):
    build = ForeignKeyField(db_column='build_id', rel_model=CiBuilds, to_field='id')
    chunk_index = IntegerField()
    data_store = IntegerField()
    id = BigIntegerField(primary_key=True)
    raw_data = BlobField(null=True)

    class Meta:
        db_table = 'ci_build_trace_chunks'
        indexes = (
            (('build', 'chunk_index'), True),
        )

class CiBuildTraceSectionNames(BaseModel):
    name = CharField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')

    class Meta:
        db_table = 'ci_build_trace_section_names'
        indexes = (
            (('project', 'name'), True),
        )

class CiBuildTraceSections(BaseModel):
    build = ForeignKeyField(db_column='build_id', rel_model=CiBuilds, to_field='id')
    byte_end = BigIntegerField()
    byte_start = BigIntegerField()
    date_end = DateTimeField()
    date_start = DateTimeField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    section_name = ForeignKeyField(db_column='section_name_id', rel_model=CiBuildTraceSectionNames, to_field='id')

    class Meta:
        db_table = 'ci_build_trace_sections'
        indexes = (
            (('build', 'section_name'), True),
        )

class CiBuildsMetadata(BaseModel):
    build = ForeignKeyField(db_column='build_id', rel_model=CiBuilds, to_field='id', unique=True)
    config_options = JSONField(null=True)
    config_variables = JSONField(null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    timeout = IntegerField(null=True)
    timeout_source = IntegerField()

    class Meta:
        db_table = 'ci_builds_metadata'

class CiBuildsRunnerSession(BaseModel):
    authorization = CharField(null=True)
    build = ForeignKeyField(db_column='build_id', rel_model=CiBuilds, to_field='id', unique=True)
    certificate = CharField(null=True)
    id = BigIntegerField(primary_key=True)
    url = CharField()

    class Meta:
        db_table = 'ci_builds_runner_session'

class CiGroupVariables(BaseModel):
    created_at = DateTimeField()
    encrypted_value = TextField(null=True)
    encrypted_value_iv = CharField(null=True)
    encrypted_value_salt = CharField(null=True)
    group = ForeignKeyField(db_column='group_id', rel_model=Namespaces, to_field='id')
    key = CharField()
    masked = BooleanField()
    protected = BooleanField()
    updated_at = DateTimeField()
    value = TextField(null=True)

    class Meta:
        db_table = 'ci_group_variables'
        indexes = (
            (('key', 'group'), True),
        )

class CiJobArtifacts(BaseModel):
    created_at = DateTimeField()
    expire_at = DateTimeField(null=True)
    file = CharField(null=True)
    file_format = IntegerField(null=True)
    file_location = IntegerField(null=True)
    file_sha256 = BlobField(null=True)
    file_store = IntegerField(index=True, null=True)
    file_type = IntegerField()
    job = ForeignKeyField(db_column='job_id', rel_model=CiBuilds, to_field='id')
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    size = BigIntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'ci_job_artifacts'
        indexes = (
            (('job', 'expire_at'), False),
            (('job', 'file_type'), True),
        )

class CiPipelineChatData(BaseModel):
    chat_name = ForeignKeyField(db_column='chat_name_id', rel_model=ChatNames, to_field='id')
    id = BigIntegerField(primary_key=True)
    pipeline = ForeignKeyField(db_column='pipeline_id', rel_model=CiPipelines, to_field='id', unique=True)
    response_url = TextField()

    class Meta:
        db_table = 'ci_pipeline_chat_data'

class CiPipelineScheduleVariables(BaseModel):
    created_at = DateTimeField(null=True)
    encrypted_value = TextField(null=True)
    encrypted_value_iv = CharField(null=True)
    encrypted_value_salt = CharField(null=True)
    key = CharField()
    pipeline_schedule = ForeignKeyField(db_column='pipeline_schedule_id', rel_model=CiPipelineSchedules, to_field='id')
    updated_at = DateTimeField(null=True)
    value = TextField(null=True)

    class Meta:
        db_table = 'ci_pipeline_schedule_variables'
        indexes = (
            (('key', 'pipeline_schedule'), True),
        )

class CiPipelineVariables(BaseModel):
    encrypted_value = TextField(null=True)
    encrypted_value_iv = CharField(null=True)
    encrypted_value_salt = CharField(null=True)
    key = CharField()
    pipeline = ForeignKeyField(db_column='pipeline_id', rel_model=CiPipelines, to_field='id')
    value = TextField(null=True)

    class Meta:
        db_table = 'ci_pipeline_variables'
        indexes = (
            (('key', 'pipeline'), True),
        )

class CiRunners(BaseModel):
    access_level = IntegerField()
    active = BooleanField()
    architecture = CharField(null=True)
    contacted_at = DateTimeField(index=True, null=True)
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    ip_address = CharField(null=True)
    is_shared = BooleanField(index=True, null=True)
    locked = BooleanField(index=True)
    maximum_timeout = IntegerField(null=True)
    name = CharField(null=True)
    platform = CharField(null=True)
    revision = CharField(null=True)
    run_untagged = BooleanField()
    runner_type = IntegerField(index=True)
    token = CharField(index=True, null=True)
    token_encrypted = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    version = CharField(null=True)

    class Meta:
        db_table = 'ci_runners'

class CiRunnerNamespaces(BaseModel):
    namespace = ForeignKeyField(db_column='namespace_id', null=True, rel_model=Namespaces, to_field='id')
    runner = ForeignKeyField(db_column='runner_id', null=True, rel_model=CiRunners, to_field='id')

    class Meta:
        db_table = 'ci_runner_namespaces'
        indexes = (
            (('runner', 'namespace'), True),
        )

class CiRunnerProjects(BaseModel):
    created_at = DateTimeField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    runner = IntegerField(db_column='runner_id', index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_runner_projects'

class CiTriggers(BaseModel):
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    owner = ForeignKeyField(db_column='owner_id', null=True, rel_model=Users, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    ref = CharField(null=True)
    token = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_triggers'

class CiTriggerRequests(BaseModel):
    commit = IntegerField(db_column='commit_id', index=True, null=True)
    created_at = DateTimeField(null=True)
    trigger = ForeignKeyField(db_column='trigger_id', rel_model=CiTriggers, to_field='id')
    updated_at = DateTimeField(null=True)
    variables = TextField(null=True)

    class Meta:
        db_table = 'ci_trigger_requests'

class CiVariables(BaseModel):
    encrypted_value = TextField(null=True)
    encrypted_value_iv = CharField(null=True)
    encrypted_value_salt = CharField(null=True)
    environment_scope = CharField()
    key = CharField()
    masked = BooleanField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    protected = BooleanField()
    value = TextField(null=True)

    class Meta:
        db_table = 'ci_variables'
        indexes = (
            (('key', 'project', 'environment_scope'), True),
        )

class Clusters(BaseModel):
    cluster_type = IntegerField()
    created_at = DateTimeField()
    domain = CharField(null=True)
    enabled = BooleanField(index=True, null=True)
    environment_scope = CharField()
    managed = BooleanField()
    name = CharField()
    platform_type = IntegerField(null=True)
    provider_type = IntegerField(null=True)
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'clusters'

class ClusterGroups(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id')
    group = ForeignKeyField(db_column='group_id', rel_model=Namespaces, to_field='id')

    class Meta:
        db_table = 'cluster_groups'
        indexes = (
            (('cluster', 'group'), True),
        )

class ClusterPlatformsKubernetes(BaseModel):
    api_url = TextField(null=True)
    authorization_type = IntegerField(null=True)
    ca_cert = TextField(null=True)
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    created_at = DateTimeField()
    encrypted_password = TextField(null=True)
    encrypted_password_iv = CharField(null=True)
    encrypted_token = TextField(null=True)
    encrypted_token_iv = CharField(null=True)
    namespace = CharField(null=True)
    updated_at = DateTimeField()
    username = CharField(null=True)

    class Meta:
        db_table = 'cluster_platforms_kubernetes'

class ClusterProjects(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id')
    created_at = DateTimeField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'cluster_projects'

class ClusterProvidersGcp(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    created_at = DateTimeField()
    encrypted_access_token = TextField(null=True)
    encrypted_access_token_iv = CharField(null=True)
    endpoint = CharField(null=True)
    gcp_project = CharField(db_column='gcp_project_id')
    legacy_abac = BooleanField()
    machine_type = CharField(null=True)
    num_nodes = IntegerField()
    operation = CharField(db_column='operation_id', null=True)
    status = IntegerField(null=True)
    status_reason = TextField(null=True)
    updated_at = DateTimeField()
    zone = CharField()

    class Meta:
        db_table = 'cluster_providers_gcp'

class ClustersApplicationsCertManagers(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    created_at = DateTimeField()
    email = CharField()
    status = IntegerField()
    status_reason = TextField(null=True)
    updated_at = DateTimeField()
    version = CharField()

    class Meta:
        db_table = 'clusters_applications_cert_managers'

class ClustersApplicationsHelm(BaseModel):
    ca_cert = TextField(null=True)
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    created_at = DateTimeField()
    encrypted_ca_key = TextField(null=True)
    encrypted_ca_key_iv = TextField(null=True)
    status = IntegerField()
    status_reason = TextField(null=True)
    updated_at = DateTimeField()
    version = CharField()

    class Meta:
        db_table = 'clusters_applications_helm'

class ClustersApplicationsIngress(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    cluster_ip = CharField(null=True)
    created_at = DateTimeField()
    external_hostname = CharField(null=True)
    external_ip = CharField(null=True)
    ingress_type = IntegerField()
    status = IntegerField()
    status_reason = TextField(null=True)
    updated_at = DateTimeField()
    version = CharField()

    class Meta:
        db_table = 'clusters_applications_ingress'

class OauthApplications(BaseModel):
    created_at = DateTimeField(null=True)
    name = CharField()
    owner = IntegerField(db_column='owner_id', null=True)
    owner_type = CharField(null=True)
    redirect_uri = TextField()
    scopes = CharField()
    secret = CharField()
    trusted = BooleanField()
    uid = CharField(unique=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'oauth_applications'
        indexes = (
            (('owner', 'owner_type'), False),
        )

class ClustersApplicationsJupyter(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    created_at = DateTimeField()
    hostname = CharField(null=True)
    oauth_application = ForeignKeyField(db_column='oauth_application_id', null=True, rel_model=OauthApplications, to_field='id')
    status = IntegerField()
    status_reason = TextField(null=True)
    updated_at = DateTimeField()
    version = CharField()

    class Meta:
        db_table = 'clusters_applications_jupyter'

class ClustersApplicationsKnative(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    created_at = DateTimeField()
    external_hostname = CharField(null=True)
    external_ip = CharField(null=True)
    hostname = CharField(null=True)
    status = IntegerField()
    status_reason = TextField(null=True)
    updated_at = DateTimeField()
    version = CharField()

    class Meta:
        db_table = 'clusters_applications_knative'

class ClustersApplicationsPrometheus(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    created_at = DateTimeField()
    status = IntegerField()
    status_reason = TextField(null=True)
    updated_at = DateTimeField()
    version = CharField()

    class Meta:
        db_table = 'clusters_applications_prometheus'

class ClustersApplicationsRunners(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id', unique=True)
    created_at = DateTimeField()
    privileged = BooleanField()
    runner = ForeignKeyField(db_column='runner_id', null=True, rel_model=CiRunners, to_field='id')
    status = IntegerField()
    status_reason = TextField(null=True)
    updated_at = DateTimeField()
    version = CharField()

    class Meta:
        db_table = 'clusters_applications_runners'

class ClustersKubernetesNamespaces(BaseModel):
    cluster = ForeignKeyField(db_column='cluster_id', rel_model=Clusters, to_field='id')
    cluster_project = ForeignKeyField(db_column='cluster_project_id', null=True, rel_model=ClusterProjects, to_field='id')
    created_at = DateTimeField()
    encrypted_service_account_token = TextField(null=True)
    encrypted_service_account_token_iv = CharField(null=True)
    id = BigIntegerField(primary_key=True)
    namespace = CharField()
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    service_account_name = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'clusters_kubernetes_namespaces'
        indexes = (
            (('cluster', 'namespace'), True),
        )

class ContainerRepositories(BaseModel):
    created_at = DateTimeField()
    name = CharField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'container_repositories'
        indexes = (
            (('project', 'name'), True),
        )

class ConversationalDevelopmentIndexMetrics(BaseModel):
    created_at = DateTimeField()
    instance_boards = FloatField()
    instance_ci_pipelines = FloatField()
    instance_deployments = FloatField()
    instance_environments = FloatField()
    instance_issues = FloatField()
    instance_merge_requests = FloatField()
    instance_milestones = FloatField()
    instance_notes = FloatField()
    instance_projects_prometheus_active = FloatField()
    instance_service_desk_issues = FloatField()
    leader_boards = FloatField()
    leader_ci_pipelines = FloatField()
    leader_deployments = FloatField()
    leader_environments = FloatField()
    leader_issues = FloatField()
    leader_merge_requests = FloatField()
    leader_milestones = FloatField()
    leader_notes = FloatField()
    leader_projects_prometheus_active = FloatField()
    leader_service_desk_issues = FloatField()
    percentage_boards = FloatField()
    percentage_ci_pipelines = FloatField()
    percentage_deployments = FloatField()
    percentage_environments = FloatField()
    percentage_issues = FloatField()
    percentage_merge_requests = FloatField()
    percentage_milestones = FloatField()
    percentage_notes = FloatField()
    percentage_projects_prometheus_active = FloatField()
    percentage_service_desk_issues = FloatField()
    updated_at = DateTimeField()

    class Meta:
        db_table = 'conversational_development_index_metrics'

class DeployKeysProjects(BaseModel):
    can_push = BooleanField()
    created_at = DateTimeField(null=True)
    deploy_key = IntegerField(db_column='deploy_key_id')
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'deploy_keys_projects'

class DeployTokens(BaseModel):
    created_at = DateTimeField()
    expires_at = DateTimeField()
    name = CharField()
    read_registry = BooleanField()
    read_repository = BooleanField()
    revoked = BooleanField(null=True)
    token = CharField(unique=True)

    class Meta:
        db_table = 'deploy_tokens'
        indexes = (
            (('id', 'expires_at', 'token'), False),
        )

class Deployments(BaseModel):
    created_at = DateTimeField(index=True, null=True)
    deployable = IntegerField(db_column='deployable_id', null=True)
    deployable_type = CharField(null=True)
    environment = IntegerField(db_column='environment_id')
    finished_at = DateTimeField(null=True)
    iid = IntegerField()
    on_stop = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    ref = CharField()
    sha = CharField()
    status = IntegerField()
    tag = BooleanField()
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'deployments'
        indexes = (
            (('created_at', 'status', 'project'), False),
            (('deployable_type', 'deployable'), False),
            (('environment', 'id'), False),
            (('environment', 'project', 'iid'), False),
            (('project', 'iid'), True),
            (('status', 'environment'), False),
            (('status', 'project'), False),
        )

class Emails(BaseModel):
    confirmation_sent_at = DateTimeField(null=True)
    confirmation_token = CharField(null=True, unique=True)
    confirmed_at = DateTimeField(null=True)
    created_at = DateTimeField(null=True)
    email = CharField(unique=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True)

    class Meta:
        db_table = 'emails'

class Environments(BaseModel):
    created_at = DateTimeField(null=True)
    environment_type = CharField(null=True)
    external_url = CharField(null=True)
    name = CharField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    slug = CharField()
    state = CharField()
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'environments'
        indexes = (
            (('project', 'name'), True),
            (('project', 'slug'), True),
        )

class Events(BaseModel):
    action = IntegerField(index=True)
    author = ForeignKeyField(db_column='author_id', rel_model=Users, to_field='id')
    created_at = DateTimeField()
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    target = IntegerField(db_column='target_id', null=True)
    target_type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'events'
        indexes = (
            (('project', 'author'), False),
            (('project', 'created_at'), False),
            (('project', 'id'), False),
            (('target', 'target_type'), False),
        )

class FeatureGates(BaseModel):
    created_at = DateTimeField()
    feature_key = CharField()
    key = CharField()
    updated_at = DateTimeField()
    value = CharField(null=True)

    class Meta:
        db_table = 'feature_gates'
        indexes = (
            (('feature_key', 'key', 'value'), True),
        )

class Features(BaseModel):
    created_at = DateTimeField()
    key = CharField(unique=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'features'

class ForkNetworks(BaseModel):
    deleted_root_project_name = CharField(null=True)
    root_project = ForeignKeyField(db_column='root_project_id', null=True, rel_model=Projects, to_field='id', unique=True)

    class Meta:
        db_table = 'fork_networks'

class ForkNetworkMembers(BaseModel):
    fork_network = ForeignKeyField(db_column='fork_network_id', rel_model=ForkNetworks, to_field='id')
    forked_from_project = ForeignKeyField(db_column='forked_from_project_id', null=True, rel_model=Projects, to_field='id')
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, related_name='projects_project_set', to_field='id', unique=True)

    class Meta:
        db_table = 'fork_network_members'

class ForkedProjectLinks(BaseModel):
    created_at = DateTimeField(null=True)
    forked_from_project = IntegerField(db_column='forked_from_project_id')
    forked_to_project = ForeignKeyField(db_column='forked_to_project_id', rel_model=Projects, to_field='id', unique=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'forked_project_links'

class GpgKeys(BaseModel):
    created_at = DateTimeField()
    fingerprint = BlobField(null=True, unique=True)
    key = TextField(null=True)
    primary_keyid = BlobField(null=True, unique=True)
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'gpg_keys'

class GpgKeySubkeys(BaseModel):
    fingerprint = BlobField(null=True, unique=True)
    gpg_key = ForeignKeyField(db_column='gpg_key_id', rel_model=GpgKeys, to_field='id')
    keyid = BlobField(null=True, unique=True)

    class Meta:
        db_table = 'gpg_key_subkeys'

class GpgSignatures(BaseModel):
    commit_sha = BlobField(null=True, unique=True)
    created_at = DateTimeField()
    gpg_key = ForeignKeyField(db_column='gpg_key_id', null=True, rel_model=GpgKeys, to_field='id')
    gpg_key_primary_keyid = BlobField(index=True, null=True)
    gpg_key_subkey = ForeignKeyField(db_column='gpg_key_subkey_id', null=True, rel_model=GpgKeySubkeys, to_field='id')
    gpg_key_user_email = TextField(null=True)
    gpg_key_user_name = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    updated_at = DateTimeField()
    verification_status = IntegerField()

    class Meta:
        db_table = 'gpg_signatures'

class GroupCustomAttributes(BaseModel):
    created_at = DateTimeField()
    group = ForeignKeyField(db_column='group_id', rel_model=Namespaces, to_field='id')
    key = CharField()
    updated_at = DateTimeField()
    value = CharField()

    class Meta:
        db_table = 'group_custom_attributes'
        indexes = (
            (('group', 'key'), True),
            (('key', 'value'), False),
        )

class Identities(BaseModel):
    created_at = DateTimeField(null=True)
    extern_uid = CharField(null=True)
    provider = CharField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'identities'

class ImportExportUploads(BaseModel):
    export_file = TextField(null=True)
    import_file = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    updated_at = DateTimeField(index=True)

    class Meta:
        db_table = 'import_export_uploads'

class InternalIds(BaseModel):
    id = BigIntegerField(primary_key=True)
    last_value = IntegerField()
    namespace = ForeignKeyField(db_column='namespace_id', null=True, rel_model=Namespaces, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    usage = IntegerField()

    class Meta:
        db_table = 'internal_ids'
        indexes = (
            (('namespace', 'usage'), True),
            (('usage', 'project'), True),
        )

class Issues(BaseModel):
    author = ForeignKeyField(db_column='author_id', null=True, rel_model=Users, to_field='id')
    cached_markdown_version = IntegerField(null=True)
    closed_at = DateTimeField(null=True)
    closed_by = ForeignKeyField(db_column='closed_by_id', null=True, rel_model=Users, related_name='users_closed_by_set', to_field='id')
    confidential = BooleanField(index=True)
    created_at = DateTimeField(null=True)
    description = TextField(index=True, null=True)
    description_html = TextField(null=True)
    discussion_locked = BooleanField(null=True)
    due_date = DateField(null=True)
    iid = IntegerField(null=True)
    last_edited_at = DateTimeField(null=True)
    last_edited_by = IntegerField(db_column='last_edited_by_id', null=True)
    lock_version = IntegerField(null=True)
    milestone = ForeignKeyField(db_column='milestone_id', null=True, rel_model=Milestones, to_field='id')
    moved_to = ForeignKeyField(db_column='moved_to_id', null=True, rel_model='self', to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    relative_position = IntegerField(index=True, null=True)
    state = CharField(index=True, null=True)
    state_id = IntegerField(null=True)
    time_estimate = IntegerField(null=True)
    title = CharField(index=True, null=True)
    title_html = TextField(null=True)
    updated_at = DateTimeField(index=True, null=True)
    updated_by = ForeignKeyField(db_column='updated_by_id', null=True, rel_model=Users, related_name='users_updated_by_set', to_field='id')

    class Meta:
        db_table = 'issues'
        indexes = (
            (('id', 'project', 'created_at', 'state'), False),
            (('id', 'project', 'state', 'due_date'), False),
            (('project', 'iid'), True),
            (('updated_at', 'project', 'id', 'state'), False),
        )

class IssueAssignees(BaseModel):
    issue = ForeignKeyField(db_column='issue_id', rel_model=Issues, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'issue_assignees'
        indexes = (
            (('user', 'issue'), True),
        )
        primary_key = False

class IssueMetrics(BaseModel):
    created_at = DateTimeField()
    first_added_to_board_at = DateTimeField(null=True)
    first_associated_with_milestone_at = DateTimeField(null=True)
    first_mentioned_in_commit_at = DateTimeField(null=True)
    issue = ForeignKeyField(db_column='issue_id', rel_model=Issues, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'issue_metrics'

class Keys(BaseModel):
    created_at = DateTimeField(null=True)
    fingerprint = CharField(null=True, unique=True)
    key = TextField(null=True)
    last_used_at = DateTimeField(null=True)
    public = BooleanField()
    title = CharField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'keys'

class Labels(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    color = CharField(null=True)
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    description_html = TextField(null=True)
    group = ForeignKeyField(db_column='group_id', null=True, rel_model=Namespaces, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    template = BooleanField(index=True, null=True)
    title = CharField(index=True, null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'labels'
        indexes = (
            (('title', 'group', 'project'), True),
            (('type', 'project'), False),
        )

class LabelLinks(BaseModel):
    created_at = DateTimeField(null=True)
    label = ForeignKeyField(db_column='label_id', null=True, rel_model=Labels, to_field='id')
    target = IntegerField(db_column='target_id', null=True)
    target_type = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'label_links'
        indexes = (
            (('target', 'target_type'), False),
        )

class LabelPriorities(BaseModel):
    created_at = DateTimeField()
    label = ForeignKeyField(db_column='label_id', rel_model=Labels, to_field='id')
    priority = IntegerField(index=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'label_priorities'
        indexes = (
            (('project', 'label'), True),
        )

class LfsFileLocks(BaseModel):
    created_at = DateTimeField()
    path = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'lfs_file_locks'
        indexes = (
            (('project', 'path'), True),
        )

class LfsObjects(BaseModel):
    created_at = DateTimeField(null=True)
    file = CharField(null=True)
    file_store = IntegerField(index=True, null=True)
    oid = CharField(unique=True)
    size = BigIntegerField()
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'lfs_objects'

class LfsObjectsProjects(BaseModel):
    created_at = DateTimeField(null=True)
    lfs_object = IntegerField(db_column='lfs_object_id')
    project = IntegerField(db_column='project_id', index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'lfs_objects_projects'

class Lists(BaseModel):
    board = ForeignKeyField(db_column='board_id', rel_model=Boards, to_field='id')
    created_at = DateTimeField()
    label = ForeignKeyField(db_column='label_id', null=True, rel_model=Labels, to_field='id')
    list_type = IntegerField(index=True)
    position = IntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'lists'
        indexes = (
            (('board', 'label'), True),
        )

class Members(BaseModel):
    access_level = IntegerField(index=True)
    created_at = DateTimeField(null=True)
    created_by = IntegerField(db_column='created_by_id', null=True)
    expires_at = DateField(null=True)
    invite_accepted_at = DateTimeField(null=True)
    invite_email = CharField(null=True)
    invite_token = CharField(null=True, unique=True)
    notification_level = IntegerField()
    requested_at = DateTimeField(index=True, null=True)
    source = IntegerField(db_column='source_id')
    source_type = CharField()
    type = CharField(null=True)
    updated_at = DateTimeField(null=True)
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'members'
        indexes = (
            (('source_type', 'source'), False),
        )

class MergeRequestAssignees(BaseModel):
    merge_request = ForeignKeyField(db_column='merge_request_id', rel_model=MergeRequests, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'merge_request_assignees'
        indexes = (
            (('user', 'merge_request'), True),
        )

class MergeRequestDiffCommits(BaseModel):
    author_email = TextField(null=True)
    author_name = TextField(null=True)
    authored_date = DateTimeField(null=True)
    committed_date = DateTimeField(null=True)
    committer_email = TextField(null=True)
    committer_name = TextField(null=True)
    merge_request_diff = ForeignKeyField(db_column='merge_request_diff_id', rel_model=MergeRequestDiffs, to_field='id')
    message = TextField(null=True)
    relative_order = IntegerField()
    sha = BlobField(index=True)

    class Meta:
        db_table = 'merge_request_diff_commits'
        indexes = (
            (('merge_request_diff', 'relative_order'), True),
        )
        primary_key = False

class MergeRequestDiffFiles(BaseModel):
    a_mode = CharField()
    b_mode = CharField()
    binary = BooleanField(null=True)
    deleted_file = BooleanField()
    diff = TextField(null=True)
    external_diff_offset = IntegerField(null=True)
    external_diff_size = IntegerField(null=True)
    merge_request_diff = ForeignKeyField(db_column='merge_request_diff_id', rel_model=MergeRequestDiffs, to_field='id')
    new_file = BooleanField()
    new_path = TextField()
    old_path = TextField()
    relative_order = IntegerField()
    renamed_file = BooleanField()
    too_large = BooleanField()

    class Meta:
        db_table = 'merge_request_diff_files'
        indexes = (
            (('merge_request_diff', 'relative_order'), True),
        )
        primary_key = False

class MergeRequestMetrics(BaseModel):
    created_at = DateTimeField()
    first_deployed_to_production_at = DateTimeField(index=True, null=True)
    latest_build_finished_at = DateTimeField(null=True)
    latest_build_started_at = DateTimeField(null=True)
    latest_closed_at = DateTimeField(index=True, null=True)
    latest_closed_by = ForeignKeyField(db_column='latest_closed_by_id', null=True, rel_model=Users, to_field='id')
    merge_request = ForeignKeyField(db_column='merge_request_id', rel_model=MergeRequests, to_field='id')
    merged_at = DateTimeField(null=True)
    merged_by = ForeignKeyField(db_column='merged_by_id', null=True, rel_model=Users, related_name='users_merged_by_set', to_field='id')
    pipeline = ForeignKeyField(db_column='pipeline_id', null=True, rel_model=CiPipelines, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'merge_request_metrics'
        indexes = (
            (('merge_request', 'merged_at'), False),
        )

class MergeRequestsClosingIssues(BaseModel):
    created_at = DateTimeField()
    issue = ForeignKeyField(db_column='issue_id', rel_model=Issues, to_field='id')
    merge_request = ForeignKeyField(db_column='merge_request_id', rel_model=MergeRequests, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'merge_requests_closing_issues'

class Notes(BaseModel):
    attachment = CharField(null=True)
    author = IntegerField(db_column='author_id', index=True, null=True)
    cached_markdown_version = IntegerField(null=True)
    change_position = TextField(null=True)
    commit = CharField(db_column='commit_id', index=True, null=True)
    created_at = DateTimeField(index=True, null=True)
    discussion = CharField(db_column='discussion_id', index=True, null=True)
    line_code = CharField(index=True, null=True)
    note = TextField(index=True, null=True)
    note_html = TextField(null=True)
    noteable = IntegerField(db_column='noteable_id', null=True)
    noteable_type = CharField(index=True, null=True)
    original_position = TextField(null=True)
    position = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    resolved_at = DateTimeField(null=True)
    resolved_by = IntegerField(db_column='resolved_by_id', null=True)
    resolved_by_push = BooleanField(null=True)
    st_diff = TextField(null=True)
    system = BooleanField()
    type = CharField(null=True)
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(db_column='updated_by_id', null=True)

    class Meta:
        db_table = 'notes'
        indexes = (
            (('noteable', 'noteable_type'), False),
            (('noteable_type', 'project'), False),
        )

class NoteDiffFiles(BaseModel):
    a_mode = CharField()
    b_mode = CharField()
    deleted_file = BooleanField()
    diff = TextField()
    diff_note = ForeignKeyField(db_column='diff_note_id', rel_model=Notes, to_field='id', unique=True)
    new_file = BooleanField()
    new_path = TextField()
    old_path = TextField()
    renamed_file = BooleanField()

    class Meta:
        db_table = 'note_diff_files'

class NotificationSettings(BaseModel):
    close_issue = BooleanField(null=True)
    close_merge_request = BooleanField(null=True)
    created_at = DateTimeField()
    failed_pipeline = BooleanField(null=True)
    issue_due = BooleanField(null=True)
    level = IntegerField()
    merge_merge_request = BooleanField(null=True)
    new_issue = BooleanField(null=True)
    new_merge_request = BooleanField(null=True)
    new_note = BooleanField(null=True)
    push_to_merge_request = BooleanField(null=True)
    reassign_issue = BooleanField(null=True)
    reassign_merge_request = BooleanField(null=True)
    reopen_issue = BooleanField(null=True)
    reopen_merge_request = BooleanField(null=True)
    source = IntegerField(db_column='source_id', null=True)
    source_type = CharField(null=True)
    success_pipeline = BooleanField(null=True)
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'notification_settings'
        indexes = (
            (('source', 'source_type'), False),
            (('source', 'source_type', 'user'), True),
        )

class OauthAccessGrants(BaseModel):
    application = IntegerField(db_column='application_id')
    created_at = DateTimeField()
    expires_in = IntegerField()
    redirect_uri = TextField()
    resource_owner = IntegerField(db_column='resource_owner_id')
    revoked_at = DateTimeField(null=True)
    scopes = CharField(null=True)
    token = CharField(unique=True)

    class Meta:
        db_table = 'oauth_access_grants'

class OauthAccessTokens(BaseModel):
    application = IntegerField(db_column='application_id', null=True)
    created_at = DateTimeField()
    expires_in = IntegerField(null=True)
    refresh_token = CharField(null=True, unique=True)
    resource_owner = IntegerField(db_column='resource_owner_id', index=True, null=True)
    revoked_at = DateTimeField(null=True)
    scopes = CharField(null=True)
    token = CharField(unique=True)

    class Meta:
        db_table = 'oauth_access_tokens'

class OauthOpenidRequests(BaseModel):
    access_grant = ForeignKeyField(db_column='access_grant_id', rel_model=OauthAccessGrants, to_field='id')
    nonce = CharField()

    class Meta:
        db_table = 'oauth_openid_requests'

class PagesDomains(BaseModel):
    certificate = TextField(null=True)
    domain = CharField(null=True, unique=True)
    enabled_until = DateTimeField(null=True)
    encrypted_key = TextField(null=True)
    encrypted_key_iv = CharField(null=True)
    encrypted_key_salt = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    verification_code = CharField()
    verified_at = DateTimeField(index=True, null=True)

    class Meta:
        db_table = 'pages_domains'
        indexes = (
            (('project', 'enabled_until'), False),
            (('verified_at', 'enabled_until'), False),
        )

class PersonalAccessTokens(BaseModel):
    created_at = DateTimeField()
    expires_at = DateField(null=True)
    impersonation = BooleanField()
    name = CharField()
    revoked = BooleanField(null=True)
    scopes = CharField()
    token_digest = CharField(null=True, unique=True)
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'personal_access_tokens'

class ProgrammingLanguages(BaseModel):
    color = CharField()
    created_at = DateTimeField()
    name = CharField(unique=True)

    class Meta:
        db_table = 'programming_languages'

class ProjectAuthorizations(BaseModel):
    access_level = IntegerField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'project_authorizations'
        indexes = (
            (('user', 'project', 'access_level'), True),
        )
        primary_key = False

class ProjectAutoDevops(BaseModel):
    created_at = DateTimeField()
    deploy_strategy = IntegerField()
    domain = CharField(null=True)
    enabled = BooleanField(null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id', unique=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'project_auto_devops'

class ProjectCiCdSettings(BaseModel):
    group_runners_enabled = BooleanField()
    merge_pipelines_enabled = BooleanField(null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id', unique=True)

    class Meta:
        db_table = 'project_ci_cd_settings'

class ProjectCustomAttributes(BaseModel):
    created_at = DateTimeField()
    key = CharField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField()
    value = CharField()

    class Meta:
        db_table = 'project_custom_attributes'
        indexes = (
            (('key', 'value'), False),
            (('project', 'key'), True),
        )

class ProjectDailyStatistics(BaseModel):
    date = DateField(null=True)
    fetch_count = IntegerField()
    id = BigIntegerField(primary_key=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')

    class Meta:
        db_table = 'project_daily_statistics'
        indexes = (
            (('project', 'date'), True),
        )

class ProjectDeployTokens(BaseModel):
    created_at = DateTimeField()
    deploy_token = ForeignKeyField(db_column='deploy_token_id', rel_model=DeployTokens, to_field='id')
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')

    class Meta:
        db_table = 'project_deploy_tokens'
        indexes = (
            (('project', 'deploy_token'), True),
        )

class ProjectErrorTrackingSettings(BaseModel):
    api_url = CharField(null=True)
    enabled = BooleanField()
    encrypted_token = CharField(null=True)
    encrypted_token_iv = CharField(null=True)
    organization_name = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', primary_key=True, rel_model=Projects, to_field='id')
    project_name = CharField(null=True)

    class Meta:
        db_table = 'project_error_tracking_settings'

class ProjectFeatures(BaseModel):
    builds_access_level = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    issues_access_level = IntegerField(null=True)
    merge_requests_access_level = IntegerField(null=True)
    pages_access_level = IntegerField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id', unique=True)
    repository_access_level = IntegerField()
    snippets_access_level = IntegerField()
    updated_at = DateTimeField(null=True)
    wiki_access_level = IntegerField(null=True)

    class Meta:
        db_table = 'project_features'

class ProjectGroupLinks(BaseModel):
    created_at = DateTimeField(null=True)
    expires_at = DateField(null=True)
    group_access = IntegerField()
    group = IntegerField(db_column='group_id', index=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'project_group_links'

class ProjectImportData(BaseModel):
    data = TextField(null=True)
    encrypted_credentials = TextField(null=True)
    encrypted_credentials_iv = CharField(null=True)
    encrypted_credentials_salt = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')

    class Meta:
        db_table = 'project_import_data'

class ProjectMirrorData(BaseModel):
    jid = CharField(index=True, null=True)
    last_error = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id', unique=True)
    status = CharField(index=True, null=True)

    class Meta:
        db_table = 'project_mirror_data'

class ProjectRepositories(BaseModel):
    disk_path = CharField(unique=True)
    id = BigIntegerField(primary_key=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id', unique=True)
    shard = ForeignKeyField(db_column='shard_id', rel_model=Shards, to_field='id')

    class Meta:
        db_table = 'project_repositories'

class ProjectStatistics(BaseModel):
    build_artifacts_size = BigIntegerField()
    commit_count = BigIntegerField()
    lfs_objects_size = BigIntegerField()
    namespace = IntegerField(db_column='namespace_id', index=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id', unique=True)
    repository_size = BigIntegerField()
    storage_size = BigIntegerField()

    class Meta:
        db_table = 'project_statistics'

class PrometheusMetrics(BaseModel):
    common = BooleanField(index=True)
    created_at = DateTimeField()
    group = IntegerField(index=True)
    identifier = CharField(null=True, unique=True)
    legend = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    query = CharField()
    title = CharField()
    unit = CharField(null=True)
    updated_at = DateTimeField()
    y_label = CharField(null=True)

    class Meta:
        db_table = 'prometheus_metrics'

class ProtectedBranches(BaseModel):
    created_at = DateTimeField(null=True)
    name = CharField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'protected_branches'

class ProtectedBranchMergeAccessLevels(BaseModel):
    access_level = IntegerField()
    created_at = DateTimeField()
    protected_branch = ForeignKeyField(db_column='protected_branch_id', rel_model=ProtectedBranches, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'protected_branch_merge_access_levels'

class ProtectedBranchPushAccessLevels(BaseModel):
    access_level = IntegerField()
    created_at = DateTimeField()
    protected_branch = ForeignKeyField(db_column='protected_branch_id', rel_model=ProtectedBranches, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'protected_branch_push_access_levels'

class ProtectedTags(BaseModel):
    created_at = DateTimeField()
    name = CharField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'protected_tags'
        indexes = (
            (('project', 'name'), True),
        )

class ProtectedTagCreateAccessLevels(BaseModel):
    access_level = IntegerField(null=True)
    created_at = DateTimeField()
    group = ForeignKeyField(db_column='group_id', null=True, rel_model=Namespaces, to_field='id')
    protected_tag = ForeignKeyField(db_column='protected_tag_id', rel_model=ProtectedTags, to_field='id')
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'protected_tag_create_access_levels'

class PushEventPayloads(BaseModel):
    action = IntegerField()
    commit_count = BigIntegerField()
    commit_from = BlobField(null=True)
    commit_title = CharField(null=True)
    commit_to = BlobField(null=True)
    event = ForeignKeyField(db_column='event_id', rel_model=Events, to_field='id', unique=True)
    ref = TextField(null=True)
    ref_type = IntegerField()

    class Meta:
        db_table = 'push_event_payloads'
        primary_key = False

class RedirectRoutes(BaseModel):
    created_at = DateTimeField()
    path = CharField(unique=True)
    source = IntegerField(db_column='source_id')
    source_type = CharField()
    updated_at = DateTimeField()

    class Meta:
        db_table = 'redirect_routes'
        indexes = (
            (('source', 'source_type'), False),
        )

class Releases(BaseModel):
    author = ForeignKeyField(db_column='author_id', null=True, rel_model=Users, to_field='id')
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    description = TextField(null=True)
    description_html = TextField(null=True)
    name = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    sha = CharField(null=True)
    tag = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'releases'
        indexes = (
            (('tag', 'project'), False),
        )

class ReleaseLinks(BaseModel):
    created_at = DateTimeField()
    id = BigIntegerField(primary_key=True)
    name = CharField()
    release = ForeignKeyField(db_column='release_id', rel_model=Releases, to_field='id')
    updated_at = DateTimeField()
    url = CharField()

    class Meta:
        db_table = 'release_links'
        indexes = (
            (('release', 'name'), True),
            (('release', 'url'), True),
        )

class RemoteMirrors(BaseModel):
    created_at = DateTimeField()
    enabled = BooleanField(null=True)
    encrypted_credentials = TextField(null=True)
    encrypted_credentials_iv = CharField(null=True)
    encrypted_credentials_salt = CharField(null=True)
    error_notification_sent = BooleanField(null=True)
    last_error = CharField(null=True)
    last_successful_update_at = DateTimeField(index=True, null=True)
    last_update_at = DateTimeField(null=True)
    last_update_started_at = DateTimeField(null=True)
    only_protected_branches = BooleanField()
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    remote_name = CharField(null=True)
    update_status = CharField(null=True)
    updated_at = DateTimeField()
    url = CharField(null=True)

    class Meta:
        db_table = 'remote_mirrors'

class RepositoryLanguages(BaseModel):
    programming_language = IntegerField(db_column='programming_language_id')
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    share = FloatField()

    class Meta:
        db_table = 'repository_languages'
        indexes = (
            (('project', 'programming_language'), True),
        )
        primary_key = False

class ResourceLabelEvents(BaseModel):
    action = IntegerField()
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField()
    id = BigIntegerField(primary_key=True)
    issue = ForeignKeyField(db_column='issue_id', null=True, rel_model=Issues, to_field='id')
    label = ForeignKeyField(db_column='label_id', null=True, rel_model=Labels, to_field='id')
    merge_request = ForeignKeyField(db_column='merge_request_id', null=True, rel_model=MergeRequests, to_field='id')
    reference = TextField(null=True)
    reference_html = TextField(null=True)
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'resource_label_events'

class Routes(BaseModel):
    created_at = DateTimeField(null=True)
    name = CharField(null=True)
    path = CharField(index=True)
    source = IntegerField(db_column='source_id')
    source_type = CharField()
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'routes'
        indexes = (
            (('source', 'source_type'), True),
        )

class SchemaMigrations(BaseModel):
    version = CharField(unique=True)

    class Meta:
        db_table = 'schema_migrations'
        primary_key = False

class SentNotifications(BaseModel):
    commit = CharField(db_column='commit_id', null=True)
    in_reply_to_discussion = CharField(db_column='in_reply_to_discussion_id', null=True)
    line_code = CharField(null=True)
    note_type = CharField(null=True)
    noteable = IntegerField(db_column='noteable_id', null=True)
    noteable_type = CharField(null=True)
    position = TextField(null=True)
    project = IntegerField(db_column='project_id', null=True)
    recipient = IntegerField(db_column='recipient_id', null=True)
    reply_key = CharField(unique=True)

    class Meta:
        db_table = 'sent_notifications'

class Services(BaseModel):
    active = BooleanField()
    category = CharField()
    commit_events = BooleanField()
    confidential_issues_events = BooleanField()
    confidential_note_events = BooleanField(null=True)
    created_at = DateTimeField()
    default = BooleanField(null=True)
    issues_events = BooleanField(null=True)
    job_events = BooleanField()
    merge_requests_events = BooleanField(null=True)
    note_events = BooleanField()
    pipeline_events = BooleanField()
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    properties = TextField(null=True)
    push_events = BooleanField(null=True)
    tag_push_events = BooleanField(null=True)
    template = BooleanField(index=True, null=True)
    title = CharField(null=True)
    type = CharField(index=True, null=True)
    updated_at = DateTimeField()
    wiki_page_events = BooleanField(null=True)

    class Meta:
        db_table = 'services'

class Snippets(BaseModel):
    author = IntegerField(db_column='author_id', index=True)
    cached_markdown_version = IntegerField(null=True)
    content = TextField(null=True)
    content_html = TextField(null=True)
    created_at = DateTimeField(null=True)
    description = TextField(null=True)
    description_html = TextField(null=True)
    file_name = CharField(index=True, null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    title = CharField(index=True, null=True)
    title_html = TextField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(index=True, null=True)
    visibility_level = IntegerField(index=True)

    class Meta:
        db_table = 'snippets'

class SpamLogs(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    noteable_type = CharField(null=True)
    recaptcha_verified = BooleanField()
    source_ip = CharField(null=True)
    submitted_as_ham = BooleanField()
    title = CharField(null=True)
    updated_at = DateTimeField()
    user_agent = CharField(null=True)
    user = IntegerField(db_column='user_id', null=True)
    via_api = BooleanField(null=True)

    class Meta:
        db_table = 'spam_logs'

class Subscriptions(BaseModel):
    created_at = DateTimeField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    subscribable = IntegerField(db_column='subscribable_id', null=True)
    subscribable_type = CharField(null=True)
    subscribed = BooleanField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'subscriptions'
        indexes = (
            (('user', 'subscribable', 'subscribable_type', 'project'), True),
        )

class Suggestions(BaseModel):
    applied = BooleanField()
    commit = CharField(db_column='commit_id', null=True)
    from_content = TextField()
    id = BigIntegerField(primary_key=True)
    lines_above = IntegerField()
    lines_below = IntegerField()
    note = ForeignKeyField(db_column='note_id', rel_model=Notes, to_field='id')
    outdated = BooleanField()
    relative_order = IntegerField()
    to_content = TextField()

    class Meta:
        db_table = 'suggestions'
        indexes = (
            (('note', 'relative_order'), True),
        )

class SystemNoteMetadata(BaseModel):
    action = CharField(null=True)
    commit_count = IntegerField(null=True)
    created_at = DateTimeField()
    note = ForeignKeyField(db_column='note_id', rel_model=Notes, to_field='id', unique=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'system_note_metadata'

class Taggings(BaseModel):
    context = CharField(null=True)
    created_at = DateTimeField(null=True)
    tag = IntegerField(db_column='tag_id', index=True, null=True)
    taggable = IntegerField(db_column='taggable_id', null=True)
    taggable_type = CharField(null=True)
    tagger = IntegerField(db_column='tagger_id', null=True)
    tagger_type = CharField(null=True)

    class Meta:
        db_table = 'taggings'
        indexes = (
            (('taggable', 'taggable_type', 'context'), False),
            (('taggable_type', 'taggable'), False),
            (('tagger', 'context', 'tagger_type', 'tag', 'taggable', 'taggable_type'), True),
        )

class Tags(BaseModel):
    name = CharField(index=True, null=True)
    taggings_count = IntegerField(null=True)

    class Meta:
        db_table = 'tags'

class TermAgreements(BaseModel):
    accepted = BooleanField()
    created_at = DateTimeField()
    term = ForeignKeyField(db_column='term_id', rel_model=ApplicationSettingTerms, to_field='id')
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'term_agreements'
        indexes = (
            (('term', 'user'), True),
        )

class Timelogs(BaseModel):
    created_at = DateTimeField()
    issue = ForeignKeyField(db_column='issue_id', null=True, rel_model=Issues, to_field='id')
    merge_request = ForeignKeyField(db_column='merge_request_id', null=True, rel_model=MergeRequests, to_field='id')
    spent_at = DateTimeField(null=True)
    time_spent = IntegerField()
    updated_at = DateTimeField()
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'timelogs'

class Todos(BaseModel):
    action = IntegerField()
    author = ForeignKeyField(db_column='author_id', rel_model=Users, to_field='id')
    commit = CharField(db_column='commit_id', index=True, null=True)
    created_at = DateTimeField(null=True)
    group = ForeignKeyField(db_column='group_id', null=True, rel_model=Namespaces, to_field='id')
    note = ForeignKeyField(db_column='note_id', null=True, rel_model=Notes, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    state = CharField()
    target = IntegerField(db_column='target_id', null=True)
    target_type = CharField()
    updated_at = DateTimeField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=Users, related_name='users_user_set', to_field='id')

    class Meta:
        db_table = 'todos'
        indexes = (
            (('id', 'user'), False),
            (('target', 'target_type'), False),
            (('user', 'id'), False),
        )

class TrendingProjects(BaseModel):
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id', unique=True)

    class Meta:
        db_table = 'trending_projects'

class U2FRegistrations(BaseModel):
    certificate = TextField(null=True)
    counter = IntegerField(null=True)
    created_at = DateTimeField()
    key_handle = CharField(index=True, null=True)
    name = CharField(null=True)
    public_key = CharField(null=True)
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'u2f_registrations'

class UntrackedFilesForUploads(BaseModel):
    path = CharField(unique=True)

    class Meta:
        db_table = 'untracked_files_for_uploads'

class Uploads(BaseModel):
    checksum = CharField(index=True, null=True)
    created_at = DateTimeField()
    model = IntegerField(db_column='model_id', null=True)
    model_type = CharField(null=True)
    mount_point = CharField(null=True)
    path = CharField()
    secret = CharField(null=True)
    size = BigIntegerField()
    store = IntegerField(index=True, null=True)
    uploader = CharField()

    class Meta:
        db_table = 'uploads'
        indexes = (
            (('model', 'model_type'), False),
            (('path', 'uploader'), False),
        )

class UserAgentDetails(BaseModel):
    created_at = DateTimeField()
    ip_address = CharField()
    subject = IntegerField(db_column='subject_id')
    subject_type = CharField()
    submitted = BooleanField()
    updated_at = DateTimeField()
    user_agent = CharField()

    class Meta:
        db_table = 'user_agent_details'
        indexes = (
            (('subject', 'subject_type'), False),
        )

class UserCallouts(BaseModel):
    feature_name = IntegerField()
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'user_callouts'
        indexes = (
            (('feature_name', 'user'), True),
        )

class UserCustomAttributes(BaseModel):
    created_at = DateTimeField()
    key = CharField()
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')
    value = CharField()

    class Meta:
        db_table = 'user_custom_attributes'
        indexes = (
            (('key', 'value'), False),
            (('user', 'key'), True),
        )

class UserInteractedProjects(BaseModel):
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'user_interacted_projects'
        indexes = (
            (('user', 'project'), True),
        )
        primary_key = False

class UserPreferences(BaseModel):
    created_at = DateTimeField()
    first_day_of_week = IntegerField(null=True)
    issue_notes_filter = IntegerField()
    issues_sort = CharField(null=True)
    merge_request_notes_filter = IntegerField()
    merge_requests_sort = CharField(null=True)
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id', unique=True)

    class Meta:
        db_table = 'user_preferences'

class UserStatuses(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    emoji = CharField()
    message = CharField(null=True)
    message_html = CharField(null=True)
    user = ForeignKeyField(db_column='user_id', primary_key=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'user_statuses'

class UserSyncedAttributesMetadata(BaseModel):
    email_synced = BooleanField(null=True)
    location_synced = BooleanField(null=True)
    name_synced = BooleanField(null=True)
    provider = CharField(null=True)
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id', unique=True)

    class Meta:
        db_table = 'user_synced_attributes_metadata'

class UsersStarProjects(BaseModel):
    created_at = DateTimeField(null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id')

    class Meta:
        db_table = 'users_star_projects'
        indexes = (
            (('project', 'user'), True),
        )

class WebHooks(BaseModel):
    confidential_issues_events = BooleanField()
    confidential_note_events = BooleanField(null=True)
    created_at = DateTimeField(null=True)
    enable_ssl_verification = BooleanField(null=True)
    encrypted_token = CharField(null=True)
    encrypted_token_iv = CharField(null=True)
    encrypted_url = CharField(null=True)
    encrypted_url_iv = CharField(null=True)
    issues_events = BooleanField()
    job_events = BooleanField()
    merge_requests_events = BooleanField()
    note_events = BooleanField()
    pipeline_events = BooleanField()
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    push_events = BooleanField()
    push_events_branch_filter = TextField(null=True)
    repository_update_events = BooleanField()
    service = IntegerField(db_column='service_id', null=True)
    tag_push_events = BooleanField(null=True)
    type = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    wiki_page_events = BooleanField()

    class Meta:
        db_table = 'web_hooks'

class WebHookLogs(BaseModel):
    created_at = DateTimeField()
    execution_duration = FloatField(null=True)
    internal_error_message = CharField(null=True)
    request_data = TextField(null=True)
    request_headers = TextField(null=True)
    response_body = TextField(null=True)
    response_headers = TextField(null=True)
    response_status = CharField(null=True)
    trigger = CharField(null=True)
    updated_at = DateTimeField()
    url = CharField(null=True)
    web_hook = ForeignKeyField(db_column='web_hook_id', rel_model=WebHooks, to_field='id')

    class Meta:
        db_table = 'web_hook_logs'
        indexes = (
            (('web_hook', 'created_at'), False),
        )

