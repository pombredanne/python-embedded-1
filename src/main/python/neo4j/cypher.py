# Copyright (c) 2002-2011 "Neo Technology,"
# Network Engine for Objects in Lund AB [http://neotechnology.com]
#
# This file is part of Neo4j.
#
# Neo4j is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from _backend import extends, ExecutionEngine, CypherParser, from_java, strings
from neo4j.util import rethrow_current_exception_as, PythonicIterator



class CypherEngine(object):

    def __init__(self,db):
        self._engine = ExecutionEngine(db)
    
    def execute(self, query):
        return ExecutionResult(self._engine.execute(query))
        
class ExecutionResult(object):
    
    def __init__(self, projection):
        self._inner = projection
        
    def __getitem__(self, key):
        try:
            return PythonicIterator(self._inner.columnAs(key))
        except:
            rethrow_current_exception_as(KeyError)
            
    def __iter__(self):
        return PythonicIterator(self._inner.iterator())
            
    def keys(self):
        return from_java(self._inner.columns())
        
    @property
    def single(self):
        return self.__iter__().single
