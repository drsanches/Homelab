import pytest

def pytest_addoption(parser):
    parser.addoption("--host", action="store", help="Host")
    parser.addoption("--ssh_port", action="store", help="SSH port")
    parser.addoption("--opened-ports", action="store", help="All opened ports")
    parser.addoption("--https-ports-ok", action="store", help="Ports to check for HTTP 200 responses (uses https)")

@pytest.fixture
def host(request):
    return request.config.getoption("--host")

@pytest.fixture
def ssh_port(request):
    return request.config.getoption("--ssh_port")

@pytest.fixture
def opened_ports(request):
    return get_int_param_set(request, "--opened-ports")

@pytest.fixture
def https_ports_ok(request):
    return get_int_param_set(request, "--https-ports-ok")

def get_int_param_set(request, param):
    return set([int(x) for x in request.config.getoption(param).split(",")])
