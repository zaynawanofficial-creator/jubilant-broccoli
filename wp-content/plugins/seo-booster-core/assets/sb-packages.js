/* SEO Booster — accessible package-group tabs (WAI-ARIA tabs pattern, manual activation on click, arrow-key roving focus). */
( function () {
	'use strict';
	document.querySelectorAll( '.sb-packages [role="tablist"]' ).forEach( function ( list ) {
		var tabs = Array.prototype.slice.call( list.querySelectorAll( '[role="tab"]' ) );
		function select( tab, focus ) {
			tabs.forEach( function ( t ) {
				var on = t === tab;
				t.setAttribute( 'aria-selected', on ? 'true' : 'false' );
				t.tabIndex = on ? 0 : -1;
				var panel = document.getElementById( t.getAttribute( 'aria-controls' ) );
				if ( panel ) {
					panel.hidden = ! on;
				}
			} );
			if ( focus ) {
				tab.focus();
			}
			if ( window.history && window.history.replaceState ) {
				window.history.replaceState( null, '', '#' + tab.id );
			}
		}
		tabs.forEach( function ( tab, i ) {
			tab.addEventListener( 'click', function () {
				select( tab, false );
			} );
			tab.addEventListener( 'keydown', function ( e ) {
				var n = null;
				if ( e.key === 'ArrowRight' ) {
					n = tabs[ ( i + 1 ) % tabs.length ];
				} else if ( e.key === 'ArrowLeft' ) {
					n = tabs[ ( i - 1 + tabs.length ) % tabs.length ];
				} else if ( e.key === 'Home' ) {
					n = tabs[ 0 ];
				} else if ( e.key === 'End' ) {
					n = tabs[ tabs.length - 1 ];
				}
				if ( n ) {
					e.preventDefault();
					select( n, true );
				}
			} );
		} );
		// Deep link: /services/off-page-seo/#sbp-1-tab-1 opens that group.
		var hashTab = location.hash && document.getElementById( location.hash.slice( 1 ) );
		if ( hashTab && tabs.indexOf( hashTab ) > -1 ) {
			select( hashTab, false );
		}
	} );
} )();

/* Package picker: tier list (radiogroup) switches the detail panel. Arrow keys move the selection. */
( function () {
	'use strict';
	document.querySelectorAll( '[data-sb-pk]' ).forEach( function ( box ) {
		var tiers = Array.prototype.slice.call( box.querySelectorAll( '[role="radio"]' ) );
		function pick( t, focus ) {
			tiers.forEach( function ( x ) {
				var on = x === t;
				x.setAttribute( 'aria-checked', on ? 'true' : 'false' );
				x.tabIndex = on ? 0 : -1;
				var panel = document.getElementById( x.getAttribute( 'data-panel' ) );
				if ( panel ) {
					panel.hidden = ! on;
				}
			} );
			if ( focus ) {
				t.focus();
			}
			if ( window.matchMedia && window.matchMedia( '(max-width: 781px)' ).matches ) {
				var p = document.getElementById( t.getAttribute( 'data-panel' ) );
				if ( p && p.getBoundingClientRect().top > window.innerHeight * 0.75 ) {
					p.scrollIntoView( { behavior: 'smooth', block: 'start' } );
				}
			}
		}
		tiers.forEach( function ( t, i ) {
			t.addEventListener( 'click', function () { pick( t, false ); } );
			t.addEventListener( 'keydown', function ( e ) {
				var n = null;
				if ( e.key === 'ArrowDown' || e.key === 'ArrowRight' ) { n = tiers[ ( i + 1 ) % tiers.length ]; }
				if ( e.key === 'ArrowUp' || e.key === 'ArrowLeft' ) { n = tiers[ ( i - 1 + tiers.length ) % tiers.length ]; }
				if ( n ) { e.preventDefault(); pick( n, true ); }
			} );
		} );
	} );
} )();
