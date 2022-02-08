# -*- coding: utf-8 -*-
import click
import sys
import time
import json


def ftime(seconds):
    m = seconds//60
    s = seconds - m*60
    format_m = str(m) if m >= 10 else f'0{m}'
    format_s = str(s) if s >= 10 else f'0{s}'
    return f'{format_m}:{format_s}'


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--list-modes', '-l', is_flag=True, help='List pomodoro modes')
def main(ctx, list_modes):
    '''Pomodoro timer in terminal'''
    if ctx.invoked_subcommand is None:
        if list_modes:
            with open('modes.json', 'r') as f:
                modes = json.load(f)
                for i in modes.keys():
                    click.secho(f'{i}:', fg='green')
                    for j in modes[i].keys():
                        click.echo(f'\t{j}: {modes[i][j]}')


@main.command()
@click.option('--mode', '-m', default='default',
              help='Mode for pomodoro timer', show_default=True)
@click.option('--session-size', '-s', default=5,
              help='Sets session size in pomodoros', show_default=True,
              type=click.IntRange(1, 20))
@click.option('--work-label', '-w', default='It`s time for work!',
              help='Sets work time label', show_default=True)
@click.option('--break-label', '-b', default='It`s time for break!',
              help='Sets break time label', show_default=True)
def start(mode, session_size, work_label, break_label):
    '''Starts a pomodoro timer with choosed mode and size'''
    # TODO: Support long breaks
    with open('modes.json', 'r') as f:
        json_inner = f.read()
        if mode not in json.loads(json_inner).keys():
            raise NameError(f'Mode "{mode}" does not exists')
        else:
            mode_data = json.loads(json_inner)[mode]

    click.secho(
        f'Pomodoro timer with mode {mode} and session size {session_size} pomodoros launched!',
        fg='green')
    for i in range(1, session_size+1):
        click.echo('\n' + '#' * 30)
        click.secho(f'Pomodoro {i}/5 started!', fg='green')
        click.secho(work_label, fg='green')
        # For testing i use seconds instead of minutes
        for tick in range(1, mode_data['work_time']+1):
            sys.stdout.write("\r")
            sys.stdout.write(ftime(seconds=tick))
            sys.stdout.flush()
            time.sleep(1)
        # For last pomodoro
        if i < session_size:
            click.secho('\n' + break_label, fg='red')
            for tick in range(1, mode_data['break_time']+1):
                sys.stdout.write("\r")
                sys.stdout.write(ftime(seconds=tick))
                sys.stdout.flush()
                time.sleep(1)
    click.echo('\nThank you for using shellodoro! :)')


if __name__ == '__main__':
    main()
