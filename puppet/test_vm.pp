$test_packages = [
    "git",
    "vim",
    "htop",
    "python-gevent",
    "python-flask",
    "python-pip",
    "python-software-properties",
]

package { $test_packages:
    ensure  => latest,
    require => Exec["apt_update"],
}

exec {"/usr/bin/apt-get update && /usr/bin/touch /var/tmp/updated":
    alias   => "apt_update",
    creates => "/var/tmp/updated",
}

exec {"/usr/bin/pip install flask-login recaptcha-client redis":
    require => [
        Package["python-flask"],
        Package["python-pip"],
    ],
    alias => "pip",
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
    notify  => Service["web"],
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
        Exec["pip"],
        File["web.conf"],
        File["bp_folder"],
    ],
    ensure  => running,
    enable  => true,
}


exec { "/usr/bin/apt-add-repository ppa:chris-lea/redis-server && /usr/bin/apt-get update":
     alias   => "ppa_redis",
     require => Package["python-software-properties"],
     creates => "/etc/apt/sources.list.d/chris-lea-redis-server-precise.list",
 }

package {"redis-server":
    require => [
        Exec["ppa_redis"],
    ],
    ensure  => latest,
}

service {"redis-server":
    require => [
        Package["redis-server"],
        File["/etc/redis/redis.conf"],
    ],
    ensure => running,
    enable => true,
    hasstatus => true,
    hasrestart => true,
}

file {"/etc/redis/redis.conf":
    alias   => "redis.conf",
    ensure  => present,
    mode    => 0644,
    owner   => root,
    source  => "/configs/redis.conf",
    notify  => Service["redis-server"],
    require => Package["redis-server"]
}
