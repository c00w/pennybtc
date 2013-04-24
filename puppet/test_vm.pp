$test_packages = [
    "git",
    "vim",
    "htop",
    "python-gevent",
    "python-flask",
    "python-pip",
]

package { $test_packages:
    ensure => latest,
}

exec {"/usr/bin/pip install flask-login":
    require => [
        Package["python-flask"],
        Package["python-pip"],
    ],
    alias => "flask-login",
}

user {"webserver":
    home => "/home/webserver",
    ensure => present,
    managehome => true,
}

file {"/home/webserver/bp":
    require => User["webserver"],
    ensure  => directory,
    source  => "/bp",
    alias   => "bp_folder",
    owner   => "webserver",
    mode    => "0644",
    recurse => true,
    purge   => true,
    force   => true,
}

file {"/etc/init/web.conf":
    ensure  => present,
    mode    => 0644,
    source  => '/configs/web.conf',
    alias   => 'web.conf',
    notify  => Service["web"],
}

service {"web":
    require => [
        Exec["flask-login"],
        File["web.conf"],
        File["bp_folder"],
    ],
    ensure  => running,
    enable  => true,
}
