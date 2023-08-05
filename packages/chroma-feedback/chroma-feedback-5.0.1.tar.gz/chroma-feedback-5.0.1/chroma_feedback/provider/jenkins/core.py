import requests
from chroma_feedback import helper
from .normalize import normalize_data

ARGS = None


def init(program):
	global ARGS

	if not ARGS:
		program.add_argument('--jenkins-host', required = True)
		program.add_argument('--jenkins-slug', action = 'append', required = True)
	ARGS = program.parse_known_args()[0]


def run():
	result = []

	for slug in ARGS.jenkins_slug:
		result.extend(fetch(ARGS.jenkins_host, slug))
	return result


def fetch(host, slug):
	response = None

	if host and slug:
		response = requests.get(host + '/job/' + slug + '/api/json')

	# process response

	if response and response.status_code == 200:
		data = helper.parse_json(response)

		if data:
			return normalize_data(data)
	return []
