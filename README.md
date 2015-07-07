
#HELPeR

HELPeR is a personal IFTTT clone because who wants to give a corporation access
to *ALL* your online accounts?!

## Screenshots
* http://i.imgur.com/t00KTOJ.png
* http://i.imgur.com/RbVSLYQ.png
* http://i.imgur.com/zPrFDw5.png

## Agents
HELPeR consists of Agents. Agents should be a python module. For the purposes
of this README we'll be discussing a hypothetical Agent called `foobar`.

### Agent Configs
If an agent needs it, a config can be created for it in the DB.

### Agent Config Views
An agent can define a views if it as a config in `foobar.view`. They will be
loaded at `/agent_config/<AGENT_CONFIG_ID>/<AGENT_VIEW>`. They must be
specified in `foobar.ACTION_CONFIG_KEYS`

ex: `/agent/1/Foo` will call `foobar.views.Foo.as_view(request, agent_config)`

The main purpose of this is to allow for building of extra view for things like
oauth. See `helper.agents.facebook.views.FBLogin` for an example

## Tasks
Agents' tasks live in `foobar.tasks`. These should be celery tasks. Tasks are
either a 'cause' and output a list of events (flat dicts) or an
'effect' which accepts a list of events do do with as it pleases.

Cause & effect tasks are paired as TaskPair objects. Each TaskPair has 2 tasks
defined, one cause and one effect, and a set options for both.

### Task execution
Tasks get called with a union of the a AgentConfig options and the relevant
options in TaskPair (eg: cause tasks get called with cause_options).

### Task views
Tasks can have a view at `foobar.views.TaskView`. They are dispatched through a
TaskPair. POSTs going to the cause view and GETs going to the effect view. Both
require a secret in the task's options to match the URL segment with the
secret.

ex: POST to `/task/6/SECRET` calls TaskPair(id=6)'s cause view

This is best combined with the Event model to accumulate events and a scheduled
cause task that loads events from the DB.
