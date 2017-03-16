desk = {'yum':[
    'gcc-c++.x86_64',
    'gdal.x86_64 gdal-devel gdal-python.x86_64',
    'python-pip',
    '*python-nose*',
    'freetype.x86_64  freetype-devel.x86_64',
    'python-devel',
    'scipy',
    'python-matplotlib.x86_64',
    'python-psycopg2.x86_64',
    'terminator',
    'vim',
    'sendmail',
    'sendmail-cf',

    'ant compat-gcc-34-g77 freetype freetype-devel zlib-devel mpich2 readline-devel zeromq zeromq-devel gsl gsl-devel libxslt libpng libpng-devel libgfortran mysql mysql-devel libXt libXt-devel libX11-devel mpich2 mpich2-devel libxml2 xorg-x11-server-Xorg dejavu* python-devel sqlite-devel tcl-devel tk-devel R R-devel ghc',

    'hipchat',
    'google-chrome-stable',
    'python-lxml.x86_64',
    'redhat-rpm-config',
    '*backintime*',

    'postgresql96*',
    'postgis2*',
    'pgadmin3.x86_64',
    'qgis.x86_64',
    'unixODBC-devel',
    'python-twisted-*'

]
    ,
'pip':[

    'fiona',
    'shapely',
    'pandas==0.16.2 scikit-learn',
    'tornado',
    'pyzmq',

    'python-pcapng==0.1a0',
    'scapy==2.3.2',
    'functools32==3.2.3.post2',
    'geojson==1.3.2',
    'httplib2==0.9.1',
    'pyproj==1.9.5.1',
    'termcolor',
    'cogent==1.5.3',
    'ipython==2.2.0',

    'python-pcapng==0.1a0',
    'imqtt',
    'mock',
    'pyodbc==3.1.1'

],
'rpm': [
'-iUvh http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm',
'-iUvh https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm',


]

}

server = {'yum':[

    'gcc-c++.x86_64',
    'gdal-devel gdal-python.x86_64',
    'pip', 'python-pip',
    'freetype.x86_64  freetype-devel.x86_64',
    'python-devel',
    'scipy',
    'python-matplotlib.x86_64',
    'python-psycopg2.x86_64 python-psycopg2-doc.x86_64',
    'postgresql96*',
    'postgis2*',
    'terminator',
    'python-lxml.x86_64',
    'unixODBC-devel',
    'python-twisted-*'

   

] ,
'pip':[
     'fiona',
    'shapely',
    'pandas==0.16.2 scikit-learn',
    'tornado',
    'pyzmq',
    'scapy==2.3.2',
    'functools32==3.2.3.post2',
    'geojson==1.3.2',
    'httplib2==0.9.1',
    'pyproj==1.9.5.1',
    'termcolor',
    'cogent==1.5.3',
    'ipython==2.2.0',
    'mock',
    'pyodbc==3.1.1'



],
'rpm': [
    '-iUvh http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm',
    '-iUvh https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm',

]

}
