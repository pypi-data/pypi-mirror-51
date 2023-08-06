# -*-encoding:utf-8 -*-

import click
import os
import json
import zipfile
import wget
import subprocess
from shutil import copy2, copytree

import sample
from wegene_utils import process_raw_genome_data


def generate_test_data(sex, age, ancestry, haplogroup,
                       genome, rsid_file, array_format, extended_file=''):
    data = {'inputs': {'format': array_format}}
    if sex == 'y':
        data['inputs']['sex'] = sample.data['inputs']['sex']
    if age == 'y':
        data['inputs']['age'] = sample.data['inputs']['age']
    if ancestry == 'y':
        data['inputs']['ancestry'] = sample.data['inputs']['ancestry']
    if haplogroup == 'y':
        data['inputs']['haplogroup'] = sample.data['inputs']['haplogroup']
    if genome == 'y':
        data['inputs']['data'] = sample.data['inputs']['data']
    elif rsid_file != '':
        rsids_fh = open(rsid_file, 'r')
        rsids = rsids_fh.readlines()
        rsids = map(lambda rsid: rsid.strip().lower(), rsids)
        rsids_fh.close()
        user_genome = process_raw_genome_data(sample.data['inputs'])
        if extended_file:
            extended_fh = open(extended_file, 'r')
            extended_data_lines = extended_fh.readlines()
            for line in extended_data_lines:
                rs, chromosome, pos, genotype = line.strip().split('\t')
                if rs in rsids:
                    user_genome[rs] = {
                        'genotype': genotype,
                        'chromosome': chromosome,
                        'position': pos
                    }
            extended_fh.close()
        for rsid in rsids:
            try:
                data['inputs'][rsid.upper()] = user_genome[rsid]['genotype']
            except:
                click.echo(click.style(rsid + ' does not exist, ignored',
                                       fg='yellow'))

    return json.dumps(data)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--project', prompt='Project Name', default='weapp-project',
              help='Name of the project')
@click.option('--language', prompt='Language to Use', default='python27',
              type=click.Choice(['python27', 'r']), help='Language of the App')
@click.option('--sex', prompt='Require Sex', type=click.Choice(['y', 'n']),
              default='y', help='Whether to require sex data')
@click.option('--age', prompt='Require Age', type=click.Choice(['y', 'n']),
              default='y', help='Whether to require age data')
@click.option('--ancestry', prompt='Require Ancestry Composition',
              type=click.Choice(['y', 'n']), default='y',
              help='Whether to require ancestry composition')
@click.option('--haplogroup', prompt='Require Haplogroup',
              type=click.Choice(['y', 'n']), default='y',
              help='Whether to require haplogroup data')
@click.option('--genome', prompt='Require Whole Genome Data',
              type=click.Choice(['y', 'n']), default='y',
              help='Whether to require whole genome data')
@click.option('--rsid_file', prompt='RSID List File', default='',
              help='A list file with rsids required separated by new line')
@click.option('--markdown', prompt='Output In Markdown Format',
              type=click.Choice(['y', 'n']), default='y',
              help='Whether to use markdown for output')
def init(project, language, sex, age, ancestry, haplogroup, genome, rsid_file, markdown):
    work_path = os.getcwd()
    lib_path = os.path.split(os.path.abspath(__file__))[0]
    project_path = work_path + '/' + project
    project_data_path = project_path + '/data'

    if markdown == 'y':
        markdown = 1
    else:
        markdown =`0`
        
    click.echo(click.style('Initializing the project...', fg='green'))

    if(os.path.isdir(project_path)):
        click.echo(click.style('Aborted. Project folder already exists!',
                               fg='red'))
        exit()

    if genome == 'y' and rsid_file != '':
        click.echo(click.style('Required whole genome ' +
                               'reguired SNP data will be ignored.',
                   fg='yellow'))

    if genome == 'n' and rsid_file != '':
        if not os.path.isfile(rsid_file):
            click.echo(click.style('Aborted. RSID list file does not exist!',
                       fg='red'))
            exit()

    click.echo(click.style('Generating scaffold scripts...', fg='green'))

    os.makedirs(project_path)
    os.makedirs(project_data_path)

    meta = {'project': project, 'language': language, 'markdown': markdown}
    meta_file = open(project_path + '/.weapp', 'w')
    meta_file.write(json.dumps(meta, indent=4))
    meta_file.close()

    if language == 'python27':
        copy2(lib_path + '/file_templates/requirements.txt', project_path)
        copy2(lib_path + '/file_templates/wegene_utils.py', project_path)
        copy2(lib_path + '/file_templates/main.py', project_path)
        copytree(lib_path + '/indexes', project_path + '/indexes')
    elif language == 'r':
        copy2(lib_path + '/file_templates/pacman.R', project_path)
        copy2(lib_path + '/file_templates/wegene_utils.R', project_path)
        copy2(lib_path + '/file_templates/main.R', project_path)
        copytree(lib_path + '/indexes', project_path + '/indexes')

    extended_data_file = ''
    if(os.path.isdir(lib_path + '/extended_data')):
        copytree(lib_path + '/extended_data', project_path + '/extended_data')
        extended_data_file = project_path + '/extended_data/extended_data.dat'

    click.echo(click.style('Generating test data...', fg='green'))

    data_file = open(project_data_path + '/data.json', 'w')
    data_file.write(generate_test_data(sex, age, ancestry, haplogroup,
                                       genome, rsid_file, 'wegene_affy_2',
                                       extended_data_file))
    data_file.close()
    click.echo(click.style('Project Initialization Completed', fg='green'))


@cli.command()
def download_extra():
    extended_data_url = 'http://wegene-upload-prod.oss-cn-hangzhou.aliyuncs.com/sample_data/extended_data.zip'
    click.echo(click.style('Downloading extended data, ' +
                           'please wait...',
               fg='green'))
    lib_path = os.path.split(os.path.abspath(__file__))[0]
    try:
        extended_data_archive = wget.download(extended_data_url, out=lib_path)
        click.echo(click.style('\nDownload completed, unpacking now...',
                   fg='green'))
        zip_file = zipfile.ZipFile(extended_data_archive)
        for names in zip_file.namelist():
            zip_file.extract(names, lib_path)
        zip_file.close()
        click.echo(click.style('Removing temp data...',
                   fg='green'))
        if os.path.exists(extended_data_archive):
            os.remove(extended_data_archive)
        click.echo(click.style('Successfully updated extended data!',
                   fg='green'))
    except Exception:
        click.echo(click.style('Failed to download extended data, ' +
                               'please try again!',
                               fg='red'))

@cli.command()
def test():
    if not os.path.isfile('.weapp'):
        click.echo(click.style('Aborted. Not a weapp project folder!',
                               fg='red'))
        exit()
    else:
        click.echo(click.style('Testing your weapp ' +
                               'using the generated testing data...\n',
                   fg='green'))
        with open('.weapp') as meta_file:
            meta = json.load(meta_file)
        language = meta['language']
        markdown = meta['markdown']

        try:
            p1 = subprocess.Popen(['cat', './data/data.json'],
                                  stdout=subprocess.PIPE)
            if language == 'python27':
                p2 = subprocess.Popen(['python', 'main.py'],
                                      stdin=p1.stdout, stdout=subprocess.PIPE)
            elif language == 'r':
                p2 = subprocess.Popen(['Rscript', 'main.R'],
                                      stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()

            click.echo(click.style('WeApp Outputs: ', fg='green'))
            if p2.stdout is not None:
                if markdown:
                    exts = ['markdown.extensions.tables']
                    result = markdown.markdown(
                        p2.stdout.read(), extensions=exts)
                    html_file = open('./test_result.html', 'w')
                    html_file.write(result)
                    html_file.close()
                else:
                    result = p2.stdout.read()
                click.echo(click.style(result + '\n', fg='yellow'))
            else:
                click.echo(click.style('None\n', fg='yellow'))

            click.echo(click.style('WeApp Errors: ', fg='green'))
            if p2.stderr is not None:
                click.echo(click.style(p2.stderr.read() + '\n', fg='red'))
            else:
                click.echo(click.style('None\n', fg='yellow'))
        except Exception as e:
            click.echo(click.style('An error has occured during the test: ',
                                   fg='red'))
            click.echo(click.style(e.stderr, fg='red'))


@cli.command()
def package():
    if not os.path.isfile('.weapp'):
        click.echo(click.style('Aborted. Not a weapp project folder!',
                               fg='red'))
        exit()
    else:
        click.echo(click.style('Archiving the weapp...', fg='green'))
        with open('.weapp') as meta_file:
            meta = json.load(meta_file)
        archive_name = meta['project'] + '.zip'
        zipf = zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED)
        for dirname, subdirs, files in os.walk('.'):
            if dirname != './data' and dirname != './indexes' \
              and dirname != './extended_data':
                zipf.write(dirname)
                for filename in files:
                    if filename != archive_name and filename != '.weapp':
                        zipf.write(os.path.join(dirname, filename))
            else:
                click.echo(click.style('Ignoring folder for local testing: '
                                       + dirname + '. Do not put your custom '
                                       + 'files under this folder',
                           fg='yellow'))
        zipf.close()
        click.echo(click.style('Archiving completed!', fg='green'))


if __name__ == '__main__':
    cli()
