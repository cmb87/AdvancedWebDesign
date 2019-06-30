from flask import Flask, render_template, url_for, request, jsonify

def redirect_url(default='home'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)