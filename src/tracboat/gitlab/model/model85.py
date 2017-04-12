from peewee import *

database_proxy = Proxy()

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database_proxy

class AbuseReports(BaseModel):
    created_at = DateTimeField(null=True)
    message = TextField(null=True)
    reporter = IntegerField(db_column='reporter_id', null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'abuse_reports'

class ApplicationSettings(BaseModel):
    admin_notification_email = CharField(null=True)
    after_sign_out_path = CharField(null=True)
    akismet_api_key = CharField(null=True)
    akismet_enabled = BooleanField(null=True)
    created_at = DateTimeField(null=True)
    default_branch_protection = IntegerField(null=True)
    default_project_visibility = IntegerField(null=True)
    default_projects_limit = IntegerField(null=True)
    default_snippet_visibility = IntegerField(null=True)
    email_author_in_body = BooleanField(null=True)
    gravatar_enabled = BooleanField(null=True)
    help_page_text = TextField(null=True)
    home_page_url = CharField(null=True)
    import_sources = TextField(null=True)
    max_artifacts_size = IntegerField()
    max_attachment_size = IntegerField()
    metrics_enabled = BooleanField(null=True)
    metrics_host = CharField(null=True)
    metrics_method_call_threshold = IntegerField(null=True)
    metrics_pool_size = IntegerField(null=True)
    metrics_port = IntegerField(null=True)
    metrics_sample_interval = IntegerField(null=True)
    metrics_timeout = IntegerField(null=True)
    recaptcha_enabled = BooleanField(null=True)
    recaptcha_private_key = CharField(null=True)
    recaptcha_site_key = CharField(null=True)
    require_two_factor_authentication = BooleanField(null=True)
    restricted_signup_domains = TextField(null=True)
    restricted_visibility_levels = TextField(null=True)
    runners_registration_token = CharField(null=True)
    sentry_dsn = CharField(null=True)
    sentry_enabled = BooleanField(null=True)
    session_expire_delay = IntegerField()
    shared_runners_enabled = BooleanField()
    sign_in_text = TextField(null=True)
    signin_enabled = BooleanField(null=True)
    signup_enabled = BooleanField(null=True)
    twitter_sharing_enabled = BooleanField(null=True)
    two_factor_grace_period = IntegerField(null=True)
    updated_at = DateTimeField(null=True)
    user_oauth_applications = BooleanField(null=True)
    version_check_enabled = BooleanField(null=True)

    class Meta:
        db_table = 'application_settings'

class AuditEvents(BaseModel):
    author = IntegerField(db_column='author_id', index=True)
    created_at = DateTimeField(null=True)
    details = TextField(null=True)
    entity = IntegerField(db_column='entity_id')
    entity_type = CharField()
    type = CharField(index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'audit_events'
        indexes = (
            (('entity', 'entity_type'), False),
        )

class BroadcastMessages(BaseModel):
    color = CharField(null=True)
    created_at = DateTimeField(null=True)
    ends_at = DateTimeField(null=True)
    font = CharField(null=True)
    message = TextField()
    starts_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'broadcast_messages'

class CiApplicationSettings(BaseModel):
    add_pusher = BooleanField(null=True)
    all_broken_builds = BooleanField(null=True)
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_application_settings'

class CiBuilds(BaseModel):
    allow_failure = BooleanField()
    artifacts_file = TextField(null=True)
    artifacts_metadata = TextField(null=True)
    commands = TextField(null=True)
    commit = IntegerField(db_column='commit_id', index=True, null=True)
    coverage = FloatField(null=True)
    created_at = DateTimeField(null=True)
    deploy = BooleanField(null=True)
    description = CharField(null=True)
    erased_at = DateTimeField(null=True)
    erased_by = IntegerField(db_column='erased_by_id', index=True, null=True)
    finished_at = DateTimeField(null=True)
    gl_project = IntegerField(db_column='gl_project_id', index=True, null=True)
    job = IntegerField(db_column='job_id', null=True)
    name = CharField(null=True)
    options = TextField(null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    ref = CharField(null=True)
    runner = IntegerField(db_column='runner_id', index=True, null=True)
    stage = CharField(null=True)
    stage_idx = IntegerField(null=True)
    started_at = DateTimeField(null=True)
    status = CharField(index=True, null=True)
    tag = BooleanField(null=True)
    target_url = CharField(null=True)
    trace = TextField(null=True)
    trigger_request = IntegerField(db_column='trigger_request_id', null=True)
    type = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'ci_builds'
        indexes = (
            (('commit', 'created_at', 'stage_idx'), False),
            (('project', 'commit'), False),
            (('type', 'commit', 'ref'), False),
            (('type', 'commit', 'status'), False),
            (('type', 'name', 'ref', 'commit'), False),
        )

class CiCommits(BaseModel):
    before_sha = CharField(null=True)
    committed_at = DateTimeField(null=True)
    created_at = DateTimeField(null=True)
    gl_project = IntegerField(db_column='gl_project_id', index=True, null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    push_data = TextField(null=True)
    ref = CharField(null=True)
    sha = CharField(index=True, null=True)
    tag = BooleanField(null=True)
    updated_at = DateTimeField(null=True)
    yaml_errors = TextField(null=True)

    class Meta:
        db_table = 'ci_commits'
        indexes = (
            (('committed_at', 'project'), False),
            (('id', 'project', 'committed_at'), False),
            (('sha', 'project'), False),
        )

class CiEvents(BaseModel):
    created_at = DateTimeField(index=True, null=True)
    description = TextField(null=True)
    is_admin = IntegerField(index=True, null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'ci_events'

class CiJobs(BaseModel):
    active = BooleanField()
    build_branches = BooleanField()
    build_tags = BooleanField()
    commands = TextField(null=True)
    created_at = DateTimeField(null=True)
    deleted_at = DateTimeField(index=True, null=True)
    job_type = CharField(null=True)
    name = CharField(null=True)
    project = IntegerField(db_column='project_id', index=True)
    refs = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_jobs'

class CiProjects(BaseModel):
    allow_git_fetch = BooleanField()
    always_build = BooleanField()
    coverage_regex = CharField(null=True)
    created_at = DateTimeField(null=True)
    default_ref = CharField(null=True)
    email_add_pusher = BooleanField()
    email_only_broken_builds = BooleanField()
    email_recipients = CharField()
    generated_yaml_config = TextField(null=True)
    gitlab = IntegerField(db_column='gitlab_id', index=True, null=True)
    name = CharField(null=True)
    path = CharField(null=True)
    polling_interval = IntegerField(null=True)
    public = BooleanField()
    shared_runners_enabled = BooleanField(index=True, null=True)
    skip_refs = CharField(null=True)
    ssh_url_to_repo = CharField(null=True)
    timeout = IntegerField()
    token = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_projects'

class CiRunnerProjects(BaseModel):
    created_at = DateTimeField(null=True)
    gl_project = IntegerField(db_column='gl_project_id', index=True, null=True)
    project = IntegerField(db_column='project_id', null=True)
    runner = IntegerField(db_column='runner_id', index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_runner_projects'

class CiRunners(BaseModel):
    active = BooleanField()
    architecture = CharField(null=True)
    contacted_at = DateTimeField(null=True)
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    is_shared = BooleanField(null=True)
    name = CharField(null=True)
    platform = CharField(null=True)
    revision = CharField(null=True)
    token = CharField(null=True)
    updated_at = DateTimeField(null=True)
    version = CharField(null=True)

    class Meta:
        db_table = 'ci_runners'

class CiServices(BaseModel):
    active = BooleanField()
    created_at = DateTimeField(null=True)
    project = IntegerField(db_column='project_id', index=True)
    properties = TextField(null=True)
    title = CharField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_services'

class CiSessions(BaseModel):
    created_at = DateTimeField(null=True)
    data = TextField(null=True)
    session = CharField(db_column='session_id', index=True)
    updated_at = DateTimeField(index=True, null=True)

    class Meta:
        db_table = 'ci_sessions'

class CiTaggings(BaseModel):
    context = CharField(null=True)
    created_at = DateTimeField(null=True)
    tag = IntegerField(db_column='tag_id', null=True)
    taggable = IntegerField(db_column='taggable_id', null=True)
    taggable_type = CharField(null=True)
    tagger = IntegerField(db_column='tagger_id', null=True)
    tagger_type = CharField(null=True)

    class Meta:
        db_table = 'ci_taggings'
        indexes = (
            (('context', 'taggable_type', 'taggable'), False),
            (('tagger', 'context', 'tagger_type', 'tag', 'taggable', 'taggable_type'), True),
        )

class CiTags(BaseModel):
    name = CharField(null=True, unique=True)
    taggings_count = IntegerField(null=True)

    class Meta:
        db_table = 'ci_tags'

class CiTriggerRequests(BaseModel):
    commit = IntegerField(db_column='commit_id', null=True)
    created_at = DateTimeField(null=True)
    trigger = IntegerField(db_column='trigger_id')
    updated_at = DateTimeField(null=True)
    variables = TextField(null=True)

    class Meta:
        db_table = 'ci_trigger_requests'

class CiTriggers(BaseModel):
    created_at = DateTimeField(null=True)
    deleted_at = DateTimeField(index=True, null=True)
    gl_project = IntegerField(db_column='gl_project_id', index=True, null=True)
    project = IntegerField(db_column='project_id', null=True)
    token = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'ci_triggers'

class CiVariables(BaseModel):
    encrypted_value = TextField(null=True)
    encrypted_value_iv = CharField(null=True)
    encrypted_value_salt = CharField(null=True)
    gl_project = IntegerField(db_column='gl_project_id', index=True, null=True)
    key = CharField(null=True)
    project = IntegerField(db_column='project_id', null=True)
    value = TextField(null=True)

    class Meta:
        db_table = 'ci_variables'

class CiWebHooks(BaseModel):
    created_at = DateTimeField(null=True)
    project = IntegerField(db_column='project_id')
    updated_at = DateTimeField(null=True)
    url = CharField()

    class Meta:
        db_table = 'ci_web_hooks'

class DeployKeysProjects(BaseModel):
    created_at = DateTimeField(null=True)
    deploy_key = IntegerField(db_column='deploy_key_id')
    project = IntegerField(db_column='project_id', index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'deploy_keys_projects'

class Emails(BaseModel):
    created_at = DateTimeField(null=True)
    email = CharField(unique=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True)

    class Meta:
        db_table = 'emails'

class Events(BaseModel):
    action = IntegerField(index=True, null=True)
    author = IntegerField(db_column='author_id', index=True, null=True)
    created_at = DateTimeField(index=True, null=True)
    data = TextField(null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    target = IntegerField(db_column='target_id', index=True, null=True)
    target_type = CharField(index=True, null=True)
    title = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'events'

class ForkedProjectLinks(BaseModel):
    created_at = DateTimeField(null=True)
    forked_from_project = IntegerField(db_column='forked_from_project_id')
    forked_to_project = IntegerField(db_column='forked_to_project_id', unique=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'forked_project_links'

class Identities(BaseModel):
    created_at = DateTimeField(null=True)
    extern_uid = CharField(null=True)
    provider = CharField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'identities'
        indexes = (
            (('id', 'created_at'), False),
        )

class Issues(BaseModel):
    assignee = IntegerField(db_column='assignee_id', index=True, null=True)
    author = IntegerField(db_column='author_id', index=True, null=True)
    branch_name = CharField(null=True)
    created_at = DateTimeField(index=True, null=True)
    description = TextField(null=True)
    iid = IntegerField(null=True)
    milestone = IntegerField(db_column='milestone_id', index=True, null=True)
    position = IntegerField(null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    state = CharField(index=True, null=True)
    title = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(db_column='updated_by_id', null=True)

    class Meta:
        db_table = 'issues'
        indexes = (
            (('id', 'created_at'), False),
            (('project', 'iid'), True),
        )

class Keys(BaseModel):
    created_at = DateTimeField(null=True)
    fingerprint = CharField(null=True)
    key = TextField(null=True)
    public = BooleanField()
    title = CharField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'keys'
        indexes = (
            (('id', 'created_at'), False),
        )

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
    color = CharField(null=True)
    created_at = DateTimeField(null=True)
    description = CharField(null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    template = BooleanField(null=True)
    title = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'labels'

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

class Members(BaseModel):
    access_level = IntegerField(index=True)
    created_at = DateTimeField(null=True)
    created_by = IntegerField(db_column='created_by_id', null=True)
    invite_accepted_at = DateTimeField(null=True)
    invite_email = CharField(null=True)
    invite_token = CharField(null=True, unique=True)
    notification_level = IntegerField()
    source = IntegerField(db_column='source_id')
    source_type = CharField()
    type = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True, null=True)

    class Meta:
        db_table = 'members'
        indexes = (
            (('id', 'created_at'), False),
            (('source', 'source_type'), False),
        )

class MergeRequestDiffs(BaseModel):
    base_commit_sha = CharField(null=True)
    created_at = DateTimeField(null=True)
    merge_request = IntegerField(db_column='merge_request_id', unique=True)
    st_commits = TextField(null=True)
    st_diffs = TextField(null=True)
    state = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'merge_request_diffs'

class MergeRequests(BaseModel):
    assignee = IntegerField(db_column='assignee_id', index=True, null=True)
    author = IntegerField(db_column='author_id', index=True, null=True)
    created_at = DateTimeField(index=True, null=True)
    description = TextField(null=True)
    iid = IntegerField(null=True)
    locked_at = DateTimeField(null=True)
    merge_commit_sha = CharField(null=True)
    merge_error = CharField(null=True)
    merge_params = TextField(null=True)
    merge_status = CharField(null=True)
    merge_user = IntegerField(db_column='merge_user_id', null=True)
    merge_when_build_succeeds = BooleanField()
    milestone = IntegerField(db_column='milestone_id', index=True, null=True)
    position = IntegerField(null=True)
    source_branch = CharField(index=True)
    source_project = IntegerField(db_column='source_project_id', index=True)
    state = CharField(null=True)
    target_branch = CharField(index=True)
    target_project = IntegerField(db_column='target_project_id')
    title = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(db_column='updated_by_id', null=True)

    class Meta:
        db_table = 'merge_requests'
        indexes = (
            (('created_at', 'id'), False),
            (('target_project', 'iid'), True),
        )

class Milestones(BaseModel):
    created_at = DateTimeField(null=True)
    description = TextField(null=True)
    due_date = DateField(index=True, null=True)
    iid = IntegerField(null=True)
    project = IntegerField(db_column='project_id', index=True)
    state = CharField(null=True)
    title = CharField(index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'milestones'
        indexes = (
            (('id', 'created_at'), False),
            (('project', 'iid'), True),
        )

class Namespaces(BaseModel):
    avatar = CharField(null=True)
    created_at = DateTimeField(null=True)
    description = CharField()
    name = CharField(unique=True)
    owner = IntegerField(db_column='owner_id', index=True, null=True)
    path = CharField(unique=True)
    type = CharField(index=True, null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'namespaces'
        indexes = (
            (('id', 'created_at'), False),
        )

class Notes(BaseModel):
    attachment = CharField(null=True)
    author = IntegerField(db_column='author_id', index=True, null=True)
    commit = CharField(db_column='commit_id', index=True, null=True)
    created_at = DateTimeField(index=True, null=True)
    is_award = BooleanField(index=True)
    line_code = CharField(index=True, null=True)
    note = TextField(null=True)
    noteable = IntegerField(db_column='noteable_id', null=True)
    noteable_type = CharField(index=True, null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    st_diff = TextField(null=True)
    system = BooleanField()
    updated_at = DateTimeField(index=True, null=True)
    updated_by = IntegerField(db_column='updated_by_id', null=True)

    class Meta:
        db_table = 'notes'
        indexes = (
            (('created_at', 'id'), False),
            (('noteable_type', 'noteable'), False),
            (('project', 'noteable_type'), False),
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
    uid = CharField(unique=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'oauth_applications'
        indexes = (
            (('owner', 'owner_type'), False),
        )

class ProjectImportData(BaseModel):
    data = TextField(null=True)
    project = IntegerField(db_column='project_id', null=True)

    class Meta:
        db_table = 'project_import_data'

class Projects(BaseModel):
    archived = BooleanField()
    avatar = CharField(null=True)
    build_allow_git_fetch = BooleanField()
    build_coverage_regex = CharField(null=True)
    build_timeout = IntegerField()
    builds_enabled = BooleanField(index=True)
    ci = IntegerField(db_column='ci_id', index=True, null=True)
    commit_count = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    creator = IntegerField(db_column='creator_id', index=True, null=True)
    description = TextField(null=True)
    import_error = TextField(null=True)
    import_source = CharField(null=True)
    import_status = CharField(null=True)
    import_type = CharField(null=True)
    import_url = CharField(null=True)
    issues_enabled = BooleanField()
    issues_tracker = CharField()
    issues_tracker_id = CharField(null=True)
    last_activity_at = DateTimeField(index=True, null=True)
    merge_requests_enabled = BooleanField()
    name = CharField(null=True)
    namespace = IntegerField(db_column='namespace_id', index=True, null=True)
    path = CharField(index=True, null=True)
    pending_delete = BooleanField(null=True)
    public_builds = BooleanField()
    repository_size = FloatField(null=True)
    runners_token = CharField(index=True, null=True)
    shared_runners_enabled = BooleanField()
    snippets_enabled = BooleanField()
    star_count = IntegerField(index=True)
    updated_at = DateTimeField(null=True)
    visibility_level = IntegerField(index=True)
    wall_enabled = BooleanField()
    wiki_enabled = BooleanField()

    class Meta:
        db_table = 'projects'
        indexes = (
            (('id', 'created_at'), False),
            (('shared_runners_enabled', 'builds_enabled'), False),
        )

class ProtectedBranches(BaseModel):
    created_at = DateTimeField(null=True)
    developers_can_push = BooleanField()
    name = CharField()
    project = IntegerField(db_column='project_id', index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'protected_branches'

class Releases(BaseModel):
    created_at = DateTimeField(null=True)
    description = TextField(null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    tag = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'releases'
        indexes = (
            (('tag', 'project'), False),
        )

class SchemaMigrations(BaseModel):
    version = CharField(unique=True)

    class Meta:
        db_table = 'schema_migrations'

class SentNotifications(BaseModel):
    commit = CharField(db_column='commit_id', null=True)
    line_code = CharField(null=True)
    noteable = IntegerField(db_column='noteable_id', null=True)
    noteable_type = CharField(null=True)
    project = IntegerField(db_column='project_id', null=True)
    recipient = IntegerField(db_column='recipient_id', null=True)
    reply_key = CharField(unique=True)

    class Meta:
        db_table = 'sent_notifications'

class Services(BaseModel):
    active = BooleanField()
    build_events = BooleanField()
    category = CharField(index=True)
    created_at = DateTimeField()
    default = BooleanField(index=True, null=True)
    issues_events = BooleanField(null=True)
    merge_requests_events = BooleanField(null=True)
    note_events = BooleanField()
    project = IntegerField(db_column='project_id', index=True, null=True)
    properties = TextField(null=True)
    push_events = BooleanField(null=True)
    tag_push_events = BooleanField(null=True)
    template = BooleanField(index=True, null=True)
    title = CharField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'services'
        indexes = (
            (('id', 'created_at'), False),
        )

class Snippets(BaseModel):
    author = IntegerField(db_column='author_id', index=True)
    content = TextField(null=True)
    created_at = DateTimeField(index=True, null=True)
    expires_at = DateTimeField(index=True, null=True)
    file_name = CharField(null=True)
    project = IntegerField(db_column='project_id', index=True, null=True)
    title = CharField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(index=True, null=True)
    visibility_level = IntegerField(index=True)

    class Meta:
        db_table = 'snippets'
        indexes = (
            (('id', 'created_at'), False),
        )

class SpamLogs(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    noteable_type = CharField(null=True)
    project = IntegerField(db_column='project_id', null=True)
    source_ip = CharField(null=True)
    title = CharField(null=True)
    updated_at = DateTimeField()
    user_agent = CharField(null=True)
    user = IntegerField(db_column='user_id', null=True)
    via_api = BooleanField(null=True)

    class Meta:
        db_table = 'spam_logs'

class Subscriptions(BaseModel):
    created_at = DateTimeField(null=True)
    subscribable = IntegerField(db_column='subscribable_id', null=True)
    subscribable_type = CharField(null=True)
    subscribed = BooleanField(null=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', null=True)

    class Meta:
        db_table = 'subscriptions'
        indexes = (
            (('user', 'subscribable', 'subscribable_type'), True),
        )

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
            (('context', 'taggable_type', 'taggable'), False),
            (('tagger', 'context', 'tagger_type', 'tag', 'taggable', 'taggable_type'), True),
        )

class Tags(BaseModel):
    name = CharField(null=True, unique=True)
    taggings_count = IntegerField(null=True)

    class Meta:
        db_table = 'tags'

class Todos(BaseModel):
    action = IntegerField()
    author = IntegerField(db_column='author_id', index=True, null=True)
    created_at = DateTimeField(null=True)
    note = IntegerField(db_column='note_id', index=True, null=True)
    project = IntegerField(db_column='project_id', index=True)
    state = CharField(index=True)
    target = IntegerField(db_column='target_id')
    target_type = CharField()
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True)

    class Meta:
        db_table = 'todos'
        indexes = (
            (('target', 'target_type'), False),
        )

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
    created_at = DateTimeField(null=True)
    created_by = IntegerField(db_column='created_by_id', null=True)
    current_sign_in_at = DateTimeField(index=True, null=True)
    current_sign_in_ip = CharField(null=True)
    dashboard = IntegerField(null=True)
    email = CharField(unique=True)
    encrypted_otp_secret = CharField(null=True)
    encrypted_otp_secret_iv = CharField(null=True)
    encrypted_otp_secret_salt = CharField(null=True)
    encrypted_password = CharField()
    failed_attempts = IntegerField(null=True)
    hide_no_password = BooleanField(null=True)
    hide_no_ssh_key = BooleanField(null=True)
    hide_project_limit = BooleanField(null=True)
    last_credential_check_at = DateTimeField(null=True)
    last_sign_in_at = DateTimeField(null=True)
    last_sign_in_ip = CharField(null=True)
    layout = IntegerField(null=True)
    ldap_email = BooleanField()
    linkedin = CharField()
    location = CharField(null=True)
    locked_at = DateTimeField(null=True)
    name = CharField(index=True, null=True)
    notification_email = CharField(null=True)
    notification_level = IntegerField()
    otp_backup_codes = TextField(null=True)
    otp_grace_period_started_at = DateTimeField(null=True)
    otp_required_for_login = BooleanField()
    password_automatically_set = BooleanField(null=True)
    password_expires_at = DateTimeField(null=True)
    project_view = IntegerField(null=True)
    projects_limit = IntegerField(null=True)
    public_email = CharField()
    remember_created_at = DateTimeField(null=True)
    reset_password_sent_at = DateTimeField(null=True)
    reset_password_token = CharField(null=True, unique=True)
    sign_in_count = IntegerField(null=True)
    skype = CharField()
    state = CharField(null=True)
    theme = IntegerField(db_column='theme_id')
    twitter = CharField()
    unconfirmed_email = CharField(null=True)
    unlock_token = CharField(null=True)
    updated_at = DateTimeField(null=True)
    username = CharField(index=True, null=True)
    website_url = CharField()

    class Meta:
        db_table = 'users'
        indexes = (
            (('id', 'created_at'), False),
        )

class UsersStarProjects(BaseModel):
    created_at = DateTimeField(null=True)
    project = IntegerField(db_column='project_id', index=True)
    updated_at = DateTimeField(null=True)
    user = IntegerField(db_column='user_id', index=True)

    class Meta:
        db_table = 'users_star_projects'
        indexes = (
            (('project', 'user'), True),
        )

class WebHooks(BaseModel):
    build_events = BooleanField()
    created_at = DateTimeField(null=True)
    enable_ssl_verification = BooleanField(null=True)
    issues_events = BooleanField()
    merge_requests_events = BooleanField()
    note_events = BooleanField()
    project = IntegerField(db_column='project_id', index=True, null=True)
    push_events = BooleanField()
    service = IntegerField(db_column='service_id', null=True)
    tag_push_events = BooleanField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField(null=True)
    url = CharField(null=True)

    class Meta:
        db_table = 'web_hooks'
        indexes = (
            (('id', 'created_at'), False),
        )
