# ##############################################################################
#  Author: echel0n <echel0n@sickrage.ca>
#  URL: https://sickrage.ca/
#  Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#  -
#  This file is part of SiCKRAGE.
#  -
#  SiCKRAGE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  -
#  SiCKRAGE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################

from sqlalchemy import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    tv_episodes = Table('tv_episodes', meta, autoload=True)

    if hasattr(tv_episodes.c, 'indexerid'):
        tv_episodes.c.indexerid.alter(name='indexer_id')
        tv_episodes.indexes.idx_tv_episodes_showid_airdate.drop()
        idx_tv_episodes_showid_airdate = Index('idx_tv_episodes_showid_airdate', 'indexer_id', 'airdate')
        idx_tv_episodes_showid_airdate.create(tv_episodes)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    tv_episodes = Table('tv_episodes', meta, autoload=True)

    if hasattr(tv_episodes.c, 'indexer_id'):
        tv_episodes.c.indexer_id.alter(name='indexerid')
        tv_episodes.indexes.idx_tv_episodes_showid_airdate.drop()
        idx_tv_episodes_showid_airdate = Index('idx_tv_episodes_showid_airdate', 'indexerid', 'airdate')
        idx_tv_episodes_showid_airdate.create(tv_episodes)

