# -*- coding: utf-8 -*-

from peewee import *

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
    header_logo = CharField(null=True)
    logo = CharField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        db_table = 'appearances'

class ApplicationSettings(BaseModel):
    admin_notification_email = CharField(null=True)
    after_sign_out_path = CharField(null=True)
    after_sign_up_text = TextField(null=True)
    after_sign_up_text_html = TextField(null=True)
    akismet_api_key = CharField(null=True)
    akismet_enabled = BooleanField(null=True)
    cached_markdown_version = IntegerField(null=True)
    clientside_sentry_dsn = CharField(null=True)
    clientside_sentry_enabled = BooleanField()
    container_registry_token_expire_delay = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    default_artifacts_expire_in = CharField()
    default_branch_protection = IntegerField(null=True)
    default_group_visibility = IntegerField(null=True)
    default_project_visibility = IntegerField(null=True)
    default_projects_limit = IntegerField(null=True)
    default_snippet_visibility = IntegerField(null=True)
    disabled_oauth_sign_in_sources = TextField(null=True)
    domain_blacklist = TextField(null=True)
    domain_blacklist_enabled = BooleanField(null=True)
    domain_whitelist = TextField(null=True)
    email_author_in_body = BooleanField(null=True)
    enabled_git_access_protocol = CharField(null=True)
    gravatar_enabled = BooleanField(null=True)
    health_check_access_token = CharField(null=True)
    help_page_hide_commercial_content = BooleanField(null=True)
    help_page_support_url = CharField(null=True)
    help_page_text = TextField(null=True)
    help_page_text_html = TextField(null=True)
    home_page_url = CharField(null=True)
    housekeeping_bitmaps_enabled = BooleanField()
    housekeeping_enabled = BooleanField()
    housekeeping_full_repack_period = IntegerField()
    housekeeping_gc_period = IntegerField()
    housekeeping_incremental_repack_period = IntegerField()
    html_emails_enabled = BooleanField(null=True)
    import_sources = TextField(null=True)
    koding_enabled = BooleanField(null=True)
    koding_url = CharField(null=True)
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
    password_authentication_enabled = BooleanField(null=True)
    performance_bar_allowed_group = IntegerField(db_column='performance_bar_allowed_group_id', null=True)
    plantuml_enabled = BooleanField(null=True)
    plantuml_url = CharField(null=True)
    polling_interval_multiplier = DecimalField()
    prometheus_metrics_enabled = BooleanField()
    recaptcha_enabled = BooleanField(null=True)
    recaptcha_private_key = CharField(null=True)
    recaptcha_site_key = CharField(null=True)
    repository_checks_enabled = BooleanField(null=True)
    repository_storages = CharField(null=True)
    require_two_factor_authentication = BooleanField(null=True)
    restricted_visibility_levels = TextField(null=True)
    runners_registration_token = CharField(null=True)
    send_user_confirmation_email = BooleanField(null=True)
    sentry_dsn = CharField(null=True)
    sentry_enabled = BooleanField(null=True)
    session_expire_delay = IntegerField()
    shared_runners_enabled = BooleanField()
    shared_runners_text = TextField(null=True)
    shared_runners_text_html = TextField(null=True)
    sidekiq_throttling_enabled = BooleanField(null=True)
    sidekiq_throttling_factor = DecimalField(null=True)
    sidekiq_throttling_queues = CharField(null=True)
    sign_in_text = TextField(null=True)
    sign_in_text_html = TextField(null=True)
    signup_enabled = BooleanField(null=True)
    terminal_max_session_time = IntegerField()
    two_factor_grace_period = IntegerField(null=True)
    unique_ips_limit_enabled = BooleanField()
    unique_ips_limit_per_user = IntegerField(null=True)
    unique_ips_limit_time_window = IntegerField(null=True)
    updated_at = DateTimeField(null=True)
    usage_ping_enabled = BooleanField()
    user_default_external = BooleanField()
    user_oauth_applications = BooleanField(null=True)
    uuid = CharField(null=True)
    version_check_enabled = BooleanField(null=True)

    class Meta:
        db_table = 'application_settings'

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

class Projects(BaseModel):
    archived = BooleanField()
    auto_cancel_pending_pipelines = IntegerField()
    avatar = CharField(null=True)
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
    has_external_issue_tracker = BooleanField(null=True)
    has_external_wiki = BooleanField(null=True)
    import_error = TextField(null=True)
    import_jid = CharField(null=True)
    import_source = CharField(null=True)
    import_status = CharField(null=True)
    import_type = CharField(null=True)
    import_url = CharField(null=True)
    last_activity_at = DateTimeField(index=True, null=True)
    last_repository_check_at = DateTimeField(null=True)
    last_repository_check_failed = BooleanField(index=True, null=True)
    last_repository_updated_at = DateTimeField(index=True, null=True)
    lfs_enabled = BooleanField(null=True)
    name = CharField(index=True, null=True)
    namespace = IntegerField(db_column='namespace_id', index=True, null=True)
    only_allow_merge_if_all_discussions_are_resolved = BooleanField(null=True)
    only_allow_merge_if_pipeline_succeeds = BooleanField()
    path = CharField(index=True, null=True)
    pending_delete = BooleanField(index=True, null=True)
    printing_merge_request_link_enabled = BooleanField()
    public_builds = BooleanField()
    repository_storage = CharField()
    request_access_enabled = BooleanField()
    runners_token = CharField(index=True, null=True)
    shared_runners_enabled = BooleanField()
    star_count = IntegerField(index=True)
    updated_at = DateTimeField(null=True)
    visibility_level = IntegerField(index=True)

    class Meta:
        db_table = 'projects'

class Boards(BaseModel):
    created_at = DateTimeField()
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'boards'

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

class Namespaces(BaseModel):
    avatar = CharField(null=True)
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField(index=True, null=True)
    deleted_at = DateTimeField(index=True, null=True)
    description = CharField()
    description_html = TextField(null=True)
    lfs_enabled = BooleanField(null=True)
    name = CharField(index=True)
    owner = IntegerField(db_column='owner_id', index=True, null=True)
    parent = IntegerField(db_column='parent_id', null=True)
    path = CharField(index=True)
    request_access_enabled = BooleanField()
    require_two_factor_authentication = BooleanField(index=True)
    share_with_group_lock = BooleanField(null=True)
    two_factor_grace_period = IntegerField()
    type = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    visibility_level = IntegerField()

    class Meta:
        db_table = 'namespaces'
        indexes = (
            (('id', 'parent'), True),
            (('name', 'parent'), True),
        )

class ChatTeams(BaseModel):
    created_at = DateTimeField()
    name = CharField(null=True)
    namespace = ForeignKeyField(db_column='namespace_id', rel_model=Namespaces, to_field='id', unique=True)
    team = CharField(db_column='team_id', null=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'chat_teams'

class Users(BaseModel):
    admin = BooleanField(index=True)
    authentication_token = CharField(null=True, unique=True)
    avatar = CharField(null=True)
    bio = CharField(null=True)
    can_create_group = BooleanField()
    can_create_team = BooleanField()
    color_scheme = IntegerField(db_column='color_scheme_id')
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
    email_provider = CharField(null=True)
    encrypted_otp_secret = CharField(null=True)
    encrypted_otp_secret_iv = CharField(null=True)
    encrypted_otp_secret_salt = CharField(null=True)
    encrypted_password = CharField()
    external = BooleanField(null=True)
    external_email = BooleanField()
    failed_attempts = IntegerField(null=True)
    ghost = BooleanField(index=True, null=True)
    hide_no_password = BooleanField(null=True)
    hide_no_ssh_key = BooleanField(null=True)
    hide_project_limit = BooleanField(null=True)
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
    project_view = IntegerField(null=True)
    projects_limit = IntegerField(null=True)
    public_email = CharField()
    remember_created_at = DateTimeField(null=True)
    require_two_factor_authentication_from_group = BooleanField()
    reset_password_sent_at = DateTimeField(null=True)
    reset_password_token = CharField(null=True, unique=True)
    rss_token = CharField(index=True, null=True)
    sign_in_count = IntegerField(null=True)
    skype = CharField()
    state = CharField(index=True, null=True)
    twitter = CharField()
    two_factor_grace_period = IntegerField()
    unconfirmed_email = CharField(null=True)
    unlock_token = CharField(null=True)
    updated_at = DateTimeField(null=True)
    username = CharField(index=True, null=True)
    website_url = CharField()

    class Meta:
        db_table = 'users'

class CiPipelineSchedules(BaseModel):
    active = BooleanField(null=True)
    created_at = DateTimeField(null=True)
    cron = CharField(null=True)
    cron_timezone = CharField(null=True)
    deleted_at = DateTimeField(null=True)
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
    created_at = DateTimeField(null=True)
    duration = IntegerField(null=True)
    finished_at = DateTimeField(null=True)
    lock_version = IntegerField(null=True)
    pipeline_schedule = ForeignKeyField(db_column='pipeline_schedule_id', null=True, rel_model=CiPipelineSchedules, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    ref = CharField(null=True)
    sha = CharField(null=True)
    source = IntegerField(null=True)
    started_at = DateTimeField(null=True)
    status = CharField(index=True, null=True)
    tag = BooleanField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)
    yaml_errors = TextField(null=True)

    class Meta:
        db_table = 'ci_pipelines'
        indexes = (
            (('sha', 'project'), False),
            (('status', 'ref', 'project'), False),
        )

class CiStages(BaseModel):
    created_at = DateTimeField(null=True)
    name = CharField(null=True)
    pipeline = ForeignKeyField(db_column='pipeline_id', null=True, rel_model=CiPipelines, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_stages'
        indexes = (
            (('pipeline', 'name'), False),
        )

class CiBuilds(BaseModel):
    allow_failure = BooleanField()
    artifacts_expire_at = DateTimeField(null=True)
    artifacts_file = TextField(null=True)
    artifacts_metadata = TextField(null=True)
    artifacts_size = BigIntegerField(null=True)
    auto_canceled_by = ForeignKeyField(db_column='auto_canceled_by_id', null=True, rel_model=CiPipelines, to_field='id')
    commands = TextField(null=True)
    commit = IntegerField(db_column='commit_id', null=True)
    coverage = FloatField(null=True)
    coverage_regex = CharField(null=True)
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    environment = CharField(null=True)
    erased_at = DateTimeField(null=True)
    erased_by = IntegerField(db_column='erased_by_id', null=True)
    finished_at = DateTimeField(null=True)
    lock_version = IntegerField(null=True)
    name = CharField(null=True)
    options = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    queued_at = DateTimeField(null=True)
    ref = CharField(null=True)
    retried = BooleanField(null=True)
    runner = IntegerField(db_column='runner_id', index=True, null=True)
    stage = CharField(null=True)
    stage_id = ForeignKeyField(db_column='stage_id', null=True, rel_model=CiStages, to_field='id')
    stage_idx = IntegerField(null=True)
    started_at = DateTimeField(null=True)
    status = CharField(index=True, null=True)
    tag = BooleanField(null=True)
    target_url = CharField(null=True)
    token = CharField(null=True, unique=True)
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
            (('created_at', 'stage_idx', 'commit'), False),
            (('name', 'type', 'commit', 'ref'), False),
            (('ref', 'commit', 'type'), False),
            (('status', 'type', 'commit'), False),
            (('type', 'runner', 'status'), False),
        )

class CiGroupVariables(BaseModel):
    created_at = DateTimeField()
    encrypted_value = TextField(null=True)
    encrypted_value_iv = CharField(null=True)
    encrypted_value_salt = CharField(null=True)
    group = ForeignKeyField(db_column='group_id', rel_model=Namespaces, to_field='id')
    key = CharField()
    protected = BooleanField()
    updated_at = DateTimeField()
    value = TextField(null=True)

    class Meta:
        db_table = 'ci_group_variables'
        indexes = (
            (('key', 'group'), True),
        )

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

class CiRunnerProjects(BaseModel):
    created_at = DateTimeField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    runner = IntegerField(db_column='runner_id', index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_runner_projects'

class CiRunners(BaseModel):
    active = BooleanField()
    architecture = CharField(null=True)
    contacted_at = DateTimeField(index=True, null=True)
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    is_shared = BooleanField(index=True, null=True)
    locked = BooleanField(index=True)
    name = CharField(null=True)
    platform = CharField(null=True)
    revision = CharField(null=True)
    run_untagged = BooleanField()
    token = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    version = CharField(null=True)

    class Meta:
        db_table = 'ci_runners'

class CiTriggers(BaseModel):
    created_at = DateTimeField(null=True)
    deleted_at = DateTimeField(null=True)
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
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    protected = BooleanField()
    value = TextField(null=True)

    class Meta:
        db_table = 'ci_variables'
        indexes = (
            (('key', 'project', 'environment_scope'), True),
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
    created_at = DateTimeField(null=True)
    deploy_key = IntegerField(db_column='deploy_key_id')
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'deploy_keys_projects'

class Deployments(BaseModel):
    created_at = DateTimeField(index=True, null=True)
    deployable = IntegerField(db_column='deployable_id', null=True)
    deployable_type = CharField(null=True)
    environment = IntegerField(db_column='environment_id')
    iid = IntegerField()
    on_stop = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    ref = CharField()
    sha = CharField()
    tag = BooleanField()
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'deployments'
        indexes = (
            (('iid', 'project'), True),
            (('iid', 'project', 'environment'), False),
        )

class Emails(BaseModel):
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
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
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
    action = IntegerField(index=True, null=True)
    author = IntegerField(db_column='author_id', index=True, null=True)
    created_at = DateTimeField(index=True, null=True)
    data = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    target = IntegerField(db_column='target_id', index=True, null=True)
    target_type = CharField(index=True, null=True)
    title = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'events'
        indexes = (
            (('id', 'project'), False),
        )

class EventsForMigration(BaseModel):
    action = IntegerField(index=True)
    author = ForeignKeyField(db_column='author_id', rel_model=Users, to_field='id')
    created_at = DateTimeField()
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    target = IntegerField(db_column='target_id', null=True)
    target_type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'events_for_migration'
        indexes = (
            (('project', 'id'), False),
            (('target_type', 'target'), False),
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

class GpgSignatures(BaseModel):
    commit_sha = BlobField(null=True, unique=True)
    created_at = DateTimeField()
    gpg_key = ForeignKeyField(db_column='gpg_key_id', null=True, rel_model=GpgKeys, to_field='id')
    gpg_key_primary_keyid = BlobField(index=True, null=True)
    gpg_key_user_email = TextField(null=True)
    gpg_key_user_name = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    updated_at = DateTimeField()
    valid_signature = BooleanField(null=True)

    class Meta:
        db_table = 'gpg_signatures'

class Identities(BaseModel):
    created_at = DateTimeField(null=True)
    extern_uid = CharField(null=True)
    provider = CharField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'identities'

class Issues(BaseModel):
    assignee = IntegerField(db_column='assignee_id', index=True, null=True)
    author = IntegerField(db_column='author_id', index=True, null=True)
    branch_name = CharField(null=True)
    cached_markdown_version = IntegerField(null=True)
    closed_at = DateTimeField(null=True)
    confidential = BooleanField(index=True, null=True)
    created_at = DateTimeField(null=True)
    deleted_at = DateTimeField(index=True, null=True)
    description = TextField(index=True, null=True)
    description_html = TextField(null=True)
    due_date = DateField(null=True)
    iid = IntegerField(null=True)
    last_edited_at = DateTimeField(null=True)
    last_edited_by = IntegerField(db_column='last_edited_by_id', null=True)
    lock_version = IntegerField(null=True)
    milestone = IntegerField(db_column='milestone_id', index=True, null=True)
    moved_to = IntegerField(db_column='moved_to_id', null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    relative_position = IntegerField(index=True, null=True)
    state = CharField(index=True, null=True)
    time_estimate = IntegerField(null=True)
    title = CharField(index=True, null=True)
    title_html = TextField(null=True)
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(db_column='updated_by_id', null=True)

    class Meta:
        db_table = 'issues'
        indexes = (
            (('due_date', 'state', 'project', 'id'), False),
            (('id', 'project', 'updated_at', 'state'), False),
            (('iid', 'project'), True),
            (('project', 'created_at', 'state', 'id'), False),
        )

class IssueAssignees(BaseModel):
    issue = ForeignKeyField(db_column='issue_id', rel_model=Issues, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'issue_assignees'
        indexes = (
            (('user', 'issue'), True),
        )

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
    can_push = BooleanField()
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

class LabelLinks(BaseModel):
    created_at = DateTimeField(null=True)
    label = IntegerField(db_column='label_id', index=True, null=True)
    target = IntegerField(db_column='target_id', null=True)
    target_type = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'label_links'
        indexes = (
            (('target', 'target_type'), False),
        )

class Labels(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    color = CharField(null=True)
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    description_html = TextField(null=True)
    group = ForeignKeyField(db_column='group_id', null=True, rel_model=Namespaces, to_field='id')
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    template = BooleanField(null=True)
    title = CharField(index=True, null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'labels'
        indexes = (
            (('title', 'group', 'project'), True),
            (('type', 'project'), False),
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

class LfsObjects(BaseModel):
    created_at = DateTimeField(null=True)
    file = CharField(null=True)
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
    list_type = IntegerField()
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
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'members'
        indexes = (
            (('source_type', 'source'), False),
        )

class MergeRequests(BaseModel):
    assignee = IntegerField(db_column='assignee_id', index=True, null=True)
    author = IntegerField(db_column='author_id', index=True, null=True)
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField(index=True, null=True)
    deleted_at = DateTimeField(index=True, null=True)
    description = TextField(index=True, null=True)
    description_html = TextField(null=True)
    head_pipeline = ForeignKeyField(db_column='head_pipeline_id', null=True, rel_model=CiPipelines, to_field='id')
    iid = IntegerField(null=True)
    in_progress_merge_commit_sha = CharField(null=True)
    last_edited_at = DateTimeField(null=True)
    last_edited_by = IntegerField(db_column='last_edited_by_id', null=True)
    lock_version = IntegerField(null=True)
    merge_commit_sha = CharField(null=True)
    merge_error = TextField(null=True)
    merge_jid = CharField(null=True)
    merge_params = TextField(null=True)
    merge_status = CharField(null=True)
    merge_user = IntegerField(db_column='merge_user_id', null=True)
    merge_when_pipeline_succeeds = BooleanField()
    milestone = IntegerField(db_column='milestone_id', index=True, null=True)
    ref_fetched = BooleanField(null=True)
    source_branch = CharField(index=True)
    source_project = IntegerField(db_column='source_project_id', index=True)
    state = CharField(null=True)
    target_branch = CharField(index=True)
    target_project = ForeignKeyField(db_column='target_project_id', rel_model=Projects, to_field='id')
    time_estimate = IntegerField(null=True)
    title = CharField(index=True, null=True)
    title_html = TextField(null=True)
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(db_column='updated_by_id', null=True)

    class Meta:
        db_table = 'merge_requests'
        indexes = (
            (('target_project', 'iid'), True),
        )

class MergeRequestDiffs(BaseModel):
    base_commit_sha = CharField(null=True)
    created_at = DateTimeField(null=True)
    head_commit_sha = CharField(null=True)
    merge_request = ForeignKeyField(db_column='merge_request_id', rel_model=MergeRequests, to_field='id')
    real_size = CharField(null=True)
    st_commits = TextField(null=True)
    st_diffs = TextField(null=True)
    start_commit_sha = CharField(null=True)
    state = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'merge_request_diffs'

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
    sha = BlobField()

    class Meta:
        db_table = 'merge_request_diff_commits'
        indexes = (
            (('merge_request_diff', 'relative_order'), True),
        )

class MergeRequestDiffFiles(BaseModel):
    a_mode = CharField()
    b_mode = CharField()
    binary = BooleanField(null=True)
    deleted_file = BooleanField()
    diff = TextField()
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

class MergeRequestMetrics(BaseModel):
    created_at = DateTimeField()
    first_deployed_to_production_at = DateTimeField(index=True, null=True)
    latest_build_finished_at = DateTimeField(null=True)
    latest_build_started_at = DateTimeField(null=True)
    merge_request = ForeignKeyField(db_column='merge_request_id', rel_model=MergeRequests, to_field='id')
    merged_at = DateTimeField(null=True)
    pipeline = ForeignKeyField(db_column='pipeline_id', null=True, rel_model=CiPipelines, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'merge_request_metrics'

class MergeRequestsClosingIssues(BaseModel):
    created_at = DateTimeField()
    issue = ForeignKeyField(db_column='issue_id', rel_model=Issues, to_field='id')
    merge_request = ForeignKeyField(db_column='merge_request_id', rel_model=MergeRequests, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'merge_requests_closing_issues'

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
    st_diff = TextField(null=True)
    system = BooleanField()
    type = CharField(null=True)
    updated_at = DateTimeField(index=True, null=True)
    updated_by = IntegerField(db_column='updated_by_id', null=True)

    class Meta:
        db_table = 'notes'
        indexes = (
            (('noteable', 'noteable_type'), False),
            (('project', 'noteable_type'), False),
        )

class NotificationSettings(BaseModel):
    close_issue = BooleanField(null=True)
    close_merge_request = BooleanField(null=True)
    created_at = DateTimeField()
    failed_pipeline = BooleanField(null=True)
    level = IntegerField()
    merge_merge_request = BooleanField(null=True)
    new_issue = BooleanField(null=True)
    new_merge_request = BooleanField(null=True)
    new_note = BooleanField(null=True)
    reassign_issue = BooleanField(null=True)
    reassign_merge_request = BooleanField(null=True)
    reopen_issue = BooleanField(null=True)
    reopen_merge_request = BooleanField(null=True)
    source = IntegerField(db_column='source_id', null=True)
    source_type = CharField(null=True)
    success_pipeline = BooleanField(null=True)
    updated_at = DateTimeField()
    user = IntegerField(db_column='user_id', index=True)

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

class OauthOpenidRequests(BaseModel):
    access_grant = ForeignKeyField(db_column='access_grant_id', rel_model=OauthAccessGrants, to_field='id')
    nonce = CharField()

    class Meta:
        db_table = 'oauth_openid_requests'

class PagesDomains(BaseModel):
    certificate = TextField(null=True)
    domain = CharField(null=True, unique=True)
    encrypted_key = TextField(null=True)
    encrypted_key_iv = CharField(null=True)
    encrypted_key_salt = CharField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')

    class Meta:
        db_table = 'pages_domains'

class PersonalAccessTokens(BaseModel):
    created_at = DateTimeField()
    expires_at = DateField(null=True)
    impersonation = BooleanField()
    name = CharField()
    revoked = BooleanField(null=True)
    scopes = CharField()
    token = CharField(unique=True)
    updated_at = DateTimeField()
    user = ForeignKeyField(db_column='user_id', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'personal_access_tokens'

class ProjectAuthorizations(BaseModel):
    access_level = IntegerField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=Users, to_field='id')

    class Meta:
        db_table = 'project_authorizations'
        indexes = (
            (('user', 'project', 'access_level'), True),
        )

class ProjectFeatures(BaseModel):
    builds_access_level = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    issues_access_level = IntegerField(null=True)
    merge_requests_access_level = IntegerField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    repository_access_level = IntegerField()
    snippets_access_level = IntegerField(null=True)
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
    event = ForeignKeyField(db_column='event_id', rel_model=EventsForMigration, to_field='id', unique=True)
    ref = TextField(null=True)
    ref_type = IntegerField()

    class Meta:
        db_table = 'push_event_payloads'

class RedirectRoutes(BaseModel):
    created_at = DateTimeField()
    path = CharField(index=True)
    source = IntegerField(db_column='source_id')
    source_type = CharField()
    updated_at = DateTimeField()

    class Meta:
        db_table = 'redirect_routes'
        indexes = (
            (('source', 'source_type'), False),
        )

class Releases(BaseModel):
    cached_markdown_version = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    description = TextField(null=True)
    description_html = TextField(null=True)
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    tag = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'releases'
        indexes = (
            (('tag', 'project'), False),
        )

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
    type = CharField(null=True)
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
    tag = IntegerField(db_column='tag_id', null=True)
    taggable = IntegerField(db_column='taggable_id', null=True)
    taggable_type = CharField(null=True)
    tagger = IntegerField(db_column='tagger_id', null=True)
    tagger_type = CharField(null=True)

    class Meta:
        db_table = 'taggings'
        indexes = (
            (('tag', 'taggable', 'taggable_type', 'tagger', 'tagger_type', 'context'), True),
            (('taggable', 'taggable_type', 'context'), False),
        )

class Tags(BaseModel):
    name = CharField(null=True, unique=True)
    taggings_count = IntegerField(null=True)

    class Meta:
        db_table = 'tags'

class Timelogs(BaseModel):
    created_at = DateTimeField()
    issue = ForeignKeyField(db_column='issue_id', null=True, rel_model=Issues, to_field='id')
    merge_request = ForeignKeyField(db_column='merge_request_id', null=True, rel_model=MergeRequests, to_field='id')
    time_spent = IntegerField()
    updated_at = DateTimeField()
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'timelogs'

class Todos(BaseModel):
    action = IntegerField()
    author = IntegerField(db_column='author_id', index=True, null=True)
    commit = CharField(db_column='commit_id', index=True, null=True)
    created_at = DateTimeField(null=True)
    note = IntegerField(db_column='note_id', index=True, null=True)
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')
    state = CharField()
    target = IntegerField(db_column='target_id', null=True)
    target_type = CharField()
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True)

    class Meta:
        db_table = 'todos'
        indexes = (
            (('target_type', 'target'), False),
        )

class TrendingProjects(BaseModel):
    project = ForeignKeyField(db_column='project_id', rel_model=Projects, to_field='id')

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

class Uploads(BaseModel):
    checksum = CharField(index=True, null=True)
    created_at = DateTimeField()
    model = IntegerField(db_column='model_id', null=True)
    model_type = CharField(null=True)
    path = CharField(index=True)
    size = BigIntegerField()
    uploader = CharField()

    class Meta:
        db_table = 'uploads'
        indexes = (
            (('model', 'model_type'), False),
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
    created_at = DateTimeField(null=True)
    enable_ssl_verification = BooleanField(null=True)
    issues_events = BooleanField()
    job_events = BooleanField()
    merge_requests_events = BooleanField()
    note_events = BooleanField()
    pipeline_events = BooleanField()
    project = ForeignKeyField(db_column='project_id', null=True, rel_model=Projects, to_field='id')
    push_events = BooleanField()
    repository_update_events = BooleanField()
    service = IntegerField(db_column='service_id', null=True)
    tag_push_events = BooleanField(null=True)
    token = CharField(null=True)
    type = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    url = CharField(null=True)
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

