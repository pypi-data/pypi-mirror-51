<%inherit file="../layouts/main.mako"/>
<%!
    import sickrage
    from sickrage.core.common import SKIPPED, WANTED, UNAIRED, ARCHIVED, IGNORED, SNATCHED, SNATCHED_PROPER, SNATCHED_BEST, FAILED
    from sickrage.core.common import Quality, qualityPresets, qualityPresetStrings, statusStrings
    from sickrage.core.common import SD
%>

<%block name="content">
    <%
        if quality_value is not None:
            initial_quality = int(quality_value)
        else:
            initial_quality = SD

        anyQualities, bestQualities = Quality.split_quality(initial_quality)
    %>

    <div class="row">
        <div class="col-lg-10 mx-auto">
            <div class="card">
                <div class="card-header">
                    <h3 class="title">${title}</h3>
                </div>

                <div class="card-body">
                    <form action="massEdit" method="post">
                        <input type="hidden" name="toEdit" value="${showList}"/>
                        <p>
                            <u>
                                ${_('Changing any settings marked with')}
                                (*) ${_('will force a refresh of the selected shows.')}
                            </u>
                        </p>

                        <fieldset class="col-lg-9 col-md-8 col-sm-8 card-text">
                            <div class="row field-pair">
                                <label for="shows">
                                    <span class="component-title">${_('Selected Shows')}</span>
                                    <span class="component-desc">
                                        % for curName in sorted(showNames):
                                            <br/><span style="font-size: 14px;">${curName}</span>
                                        % endfor
                                    </span>
                                </label>
                            </div>

                            <div class="row">
                                <span class="component-desc">
                                    ${_('Root Directories')} (*)
                                    <table class="table">
                                        <thead>
                                            <tr>
                                                <th class="text-nowrap">${_('Current')}</th>
                                                <th class="text-nowrap">${_('New')}</th>
                                                <th class="text-nowrap">-</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % for cur_dir in root_dir_list:
                                                <% cur_index = root_dir_list.index(cur_dir) %>
                                                <tr>
                                                    <td align="center">
                                                        ${cur_dir}
                                                    </td>
                                                    <td align="center" id="display_new_root_dir_${cur_index}">
                                                        ${cur_dir}
                                                    </td>
                                                    <td>
                                                        <a href="#" class="btn btn-primary btn-sm edit_root_dir"
                                                           class="edit_root_dir"
                                                           id="edit_root_dir_${cur_index}">
                                                            ${_('Edit')}
                                                        </a>
                                                        <a href="#" class="btn btn-primary btn-sm delete_root_dir"
                                                           class="delete_root_dir"
                                                           id="delete_root_dir_${cur_index}">
                                                            ${_('Delete')}
                                                        </a>
                                                        <div class="input-group">
                                                            <input type="hidden" name="orig_root_dir_${cur_index}"
                                                                   value="${cur_dir}"/>
                                                            <input type="text" style="display: none"
                                                                   name="new_root_dir_${cur_index}"
                                                                   id="new_root_dir_${cur_index}" class="new_root_dir"
                                                                   value="${cur_dir}"/>
                                                        </div>
                                                    </td>
                                                </tr>
                                            % endfor
                                        </tbody>
                                    </table>
                                </span>
                            </div>

                            <div class="row field-pair">
                                <label for="qualityPreset">
                                    <span class="component-title">${_('Preferred Quality')}</span>
                                    <span class="component-desc">
                                        <select id="qualityPreset" name="quality_preset"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep">&lt; Keep &gt;</option>
                                            <% selected = None %>
                                            <option value="0" ${('', 'selected')[quality_value is not None and quality_value not in qualityPresets]}>
                                                ${_('Custom')}
                                            </option>
                                            % for curPreset in sorted(qualityPresets):
                                                <option value="${curPreset}" ${('', 'selected')[quality_value == curPreset]}>${qualityPresetStrings[curPreset]}</option>
                                            % endfor
                                        </select>

                                        <div id="customQuality" style="padding-left: 0;">
                                            <div style="padding-right: 40px; text-align: left; float: left;">
                                                <h5>Allowed</h5>
                                                <% anyQualityList = list(filter(lambda x: x > Quality.NONE, Quality.qualityStrings)) %>
                                                <select id="anyQualities" name="anyQualities" multiple="multiple"
                                                        size="${len(anyQualityList)}"
                                                        class="form-control form-control-inline input-sm">
                                                    % for curQuality in sorted(anyQualityList):
                                                        <option value="${curQuality}" ${('', 'selected')[curQuality in anyQualities]}>${Quality.qualityStrings[curQuality]}</option>
                                                    % endfor
                                                </select>
                                            </div>

                                            <div style="text-align: left; float: left;">
                                                <h5>Preferred</h5>
                                                <% bestQualityList = list(filter(lambda x: x >= Quality.SDTV, Quality.qualityStrings)) %>
                                                <select id="bestQualities" name="bestQualities" multiple="multiple"
                                                        size="${len(bestQualityList)}"
                                                        class="form-control form-control-inline input-sm">
                                                    % for curQuality in sorted(bestQualityList):
                                                        <option value="${curQuality}" ${('', 'selected')[curQuality in bestQualities]}>${Quality.qualityStrings[curQuality]}</option>
                                                    % endfor
                                                </select>
                                            </div>
                                        </div>
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_skip_downloaded">
                                    <span class="component-title">${_('Skip downloaded')}</span>
                                    <span class="component-desc">
                                        <select id="edit_skip_downloaded" name="skip_downloaded"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep" ${('', 'selected')[skip_downloaded_value is None]}>&lt; ${_('Keep')}
                                                &gt;</option>
                                            <option value="enable" ${('', 'selected')[skip_downloaded_value == 1]}>${_('Yes')}</option>
                                            <option value="disable" ${('', 'selected')[skip_downloaded_value == 0]}>${_('No')}</option>
                                        </select>
                                        ${_('Skips updating quality of old/new downloaded episodes.')}
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_flatten_folders">
                                        <span class="component-title">${_('Season folders')} (<span
                                                class="separator">*</span>)</span>
                                    <span class="component-desc">
                                        <select id="" name="flatten_folders"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep" ${('', 'selected')[flatten_folders_value is None]}>&lt; ${_('Keep')}
                                                &gt;</option>
                                            <option value="enable" ${('', 'selected')[flatten_folders_value == 0]}>${_('Yes')}</option>
                                            <option value="disable" ${('', 'selected')[flatten_folders_value == 1]}>${_('No')}</option>
                                        </select>
                                        ${_('Group episodes by season folder (set to "No" to store in a single folder).')}
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_paused">
                                    <span class="component-title">${_('Paused')}</span>
                                    <span class="component-desc">
                                        <select id="edit_paused" name="paused"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep" ${('', 'selected')[paused_value is None]}>&lt; ${_('Keep')}
                                                &gt;</option>
                                            <option value="enable" ${('', 'selected')[paused_value == 1]}>${_('Yes')}</option>
                                            <option value="disable" ${('', 'selected')[paused_value == 0]}>${_('No')}</option>
                                        </select>
                                        ${_('Pause these shows (SickRage will not download episodes).')}
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_default_ep_status">
                                    <span class="component-title">${_('Default Episode Status')}</span>
                                    <span class="component-desc">
                                        <select id="edit_default_ep_status" name="default_ep_status"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep">&lt; ${_('Keep')} &gt;</option>
                                            % for curStatus in [WANTED, SKIPPED, IGNORED]:
                                                <option value="${curStatus}" ${('', 'selected')[curStatus == default_ep_status_value]}>${statusStrings[curStatus]}</option>
                                            % endfor
                                        </select>
                                        ${_('This will set the status for future episodes.')}
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_scene">
                                    <span class="component-title">${_('Scene Numbering')}</span>
                                    <span class="component-desc">
                                        <select id="edit_scene" name="scene"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep" ${('', 'selected')[scene_value is None]}>&lt; ${_('Keep')}
                                                &gt;</option>
                                            <option value="enable" ${('', 'selected')[scene_value == 1]}>${_('Yes')}</option>
                                            <option value="disable" ${('', 'selected')[scene_value == 0]}>${_('No')}</option>
                                        </select>
                                        ${_('Search by scene numbering (set to "No" to search by indexer numbering).')}
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_anime">
                                    <span class="component-title">${_('Anime')}</span>
                                    <span class="component-desc">
                                        <select id="edit_anime" name="anime"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep" ${('', 'selected')[anime_value is None]}>&lt; ${_('Keep')}
                                                &gt;</option>
                                            <option value="enable" ${('', 'selected')[anime_value == 1]}>${_('Yes')}</option>
                                            <option value="disable" ${('', 'selected')[anime_value == 0]}>${_('No')}</option>
                                        </select>
                                        ${_('Set if these shows are Anime and episodes are released as Show.265 rather than Show.S02E03')}
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_sports">
                                    <span class="component-title">${_('Sports')}</span>
                                    <span class="component-desc">
                                        <select id="edit_sports" name="sports"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep" ${('', 'selected')[sports_value is None]}>&lt; ${_('Keep')}
                                                &gt;</option>
                                            <option value="enable" ${('', 'selected')[sports_value == 1]}>${_('Yes')}</option>
                                            <option value="disable" ${('', 'selected')[sports_value == 0]}>${_('No')}</option>
                                        </select>
                                        ${_('Set if these shows are sporting or MMA events released as Show.03.02.2010 rather than Show.S02E03.')}
                                        <br>
                                    <span style="color:red">${_('In case of an air date conflict between regular and special episodes, the later will be ignored.')}</span>
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_air_by_date">
                                    <span class="component-title">${_('Air by date')}</span>
                                    <span class="component-desc">
                                        <select id="edit_air_by_date" name="air_by_date"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep" ${('', 'selected')[air_by_date_value is None]}>&lt; ${_('Keep')}
                                                &gt;</option>
                                            <option value="enable" ${('', 'selected')[air_by_date_value == 1]}>${_('Yes')}</option>
                                            <option value="disable" ${('', 'selected')[air_by_date_value == 0]}>${_('No')}</option>
                                        </select>
                                        ${_('Set if these shows are released as Show.03.02.2010 rather than Show.S02E03.')}
                                        <br>
                                        <span style="color:red">
                                            ${_('In case of an air date conflict between regular and special episodes, the later will be ignored.')}
                                        </span>
                                    </span>
                                </label>
                            </div>

                            <div class="row field-pair">
                                <label for="edit_subtitles">
                                    <span class="component-title">${_('Subtitles')}</span>
                                    <span class="component-desc">
                                        <select id="edit_subtitles" name="subtitles"
                                                class="form-control form-control-inline input-sm">
                                            <option value="keep" ${('', 'selected')[subtitles_value is None]}>&lt; ${_('Keep')}
                                                &gt;</option>
                                            <option value="enable" ${('', 'selected')[subtitles_value == 1]}>${_('Yes')}</option>
                                            <option value="disable" ${('', 'selected')[subtitles_value == 0]}>${_('No')}</option>
                                        </select>
                                        ${_('Search for subtitles.')}
                                    </span>
                                </label>
                            </div>
                        </fieldset>
                        <div class="row">
                            <div class="col-md-12">
                                <input id="submit" type="submit" value="${_('Save Changes')}"
                                       class="btn config_submitter button">
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</%block>
