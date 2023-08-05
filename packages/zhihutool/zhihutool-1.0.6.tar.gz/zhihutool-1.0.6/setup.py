from setuptools import setup


setup(
    name='zhihutool',
    version='1.0.6',
    packages=['ZhihuTool'],
    url='https://github.com/rcsupermanjob/ZhihuTool',
    license='GPLv3',
    author='rcsuperman',
    author_email='269680244@qq.com',
    description='An easy way to control your zhihu account ',
    long_description= 'An easy way to control your zhihu account',
    install_requires=[
        'pyQrcode==1.2.1',
        'requests==2.22.0',
        'zxing==0.9.3',
        'requests-toolbelt==0.9.1'
    ],
    keywords='zhihu',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)